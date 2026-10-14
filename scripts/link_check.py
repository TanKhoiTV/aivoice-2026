"""Check that relative Markdown links in this repository resolve.

Splitting the project across three repositories moves documentation between them,
which is exactly when relative links break and nothing notices. This check
resolves every relative link (and image) in the tracked Markdown against the
working tree and fails on the ones that point at nothing.

Deterministic and offline by design:

- links into a submodule are skipped, because CI does not check the submodule out
  (this repo tracks the benchmark as ``prototype/``);
- ``http(s)``, ``mailto`` and other schemes are counted but never fetched -- a
  network check fails for reasons that have nothing to do with this repository;
- text inside fenced code blocks is ignored, so examples cannot fail the build;
- ``#fragment`` anchors are not validated.

The module is stdlib-only and self-contained, so it runs either as
``python -m scripts.link_check`` or as a plain ``python scripts/link_check.py``.

Exit status is non-zero when a relative link does not resolve.
"""

from __future__ import annotations

import argparse
import posixpath
import re
import subprocess
import sys
from collections.abc import Sequence
from pathlib import Path, PurePosixPath
from typing import NamedTuple
from urllib.parse import unquote

REPO_ROOT = Path(__file__).resolve().parent.parent

#: ``[text](target)`` and ``![alt](target)``; the target stops at whitespace or
#: ``)`` so an optional ``"title"`` is not captured.
INLINE_LINK = re.compile(r"!?\[[^\]]*\]\(\s*([^)\s]+)")
#: ``[label]: target`` reference definitions.
REFERENCE_LINK = re.compile(r"^\s{0,3}\[[^\]]+\]:\s*(\S+)")
#: ``scheme:`` prefix, e.g. ``https:``, ``mailto:``.
SCHEME = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.\-]*:")
FENCE = re.compile(r"^\s*(```|~~~)")

#: Outcome kinds for a single link target.
EXTERNAL = "external"
ANCHOR = "anchor"
SUBMODULE = "submodule"
RESOLVED = "resolved"
MISSING = "missing"
ESCAPES = "escapes"


class Link(NamedTuple):
    """A link found in a Markdown file."""

    source: str
    line: int
    target: str


class Finding(NamedTuple):
    """A link that cannot resolve."""

    source: str
    line: int
    target: str
    why: str


def links_in(text: str, source: str) -> list[Link]:
    """Return every inline and reference link in *text*, ignoring code fences."""
    found: list[Link] = []
    fenced = False
    for number, line in enumerate(text.splitlines(), start=1):
        if FENCE.match(line):
            fenced = not fenced
            continue
        if fenced:
            continue
        for match in INLINE_LINK.finditer(line):
            found.append(Link(source, number, match.group(1)))
        reference = REFERENCE_LINK.match(line)
        if reference:
            found.append(Link(source, number, reference.group(1)))
    return found


def submodule_paths(gitmodules_text: str) -> list[str]:
    """Return the ``path`` of every section in ``.gitmodules``."""
    paths: list[str] = []
    in_section = False
    for line in gitmodules_text.splitlines():
        stripped = line.strip()
        if stripped.startswith("[submodule"):
            in_section = True
            continue
        if not in_section or not stripped.lower().startswith("path"):
            continue
        _, _, value = stripped.partition("=")
        paths.append(value.strip().strip("/"))
        in_section = False
    return paths


def classify_target(
    target: str, source: str, repo_root: Path, submodules: Sequence[str]
) -> tuple[str, str]:
    """Resolve one target to ``(kind, what it points at)``."""
    raw = target.strip()
    if raw.startswith("<") and raw.endswith(">"):
        raw = raw[1:-1]
    if SCHEME.match(raw):
        return EXTERNAL, raw
    if not raw or raw.startswith("#"):
        return ANCHOR, raw
    path_part, _, _fragment = raw.partition("#")
    path_part = unquote(path_part)
    if not path_part:
        return ANCHOR, raw
    if path_part.startswith("/"):
        # GitHub renders a leading slash relative to the repository root.
        joined = posixpath.normpath(path_part.lstrip("/"))
    else:
        joined = posixpath.normpath(
            posixpath.join(str(PurePosixPath(source).parent), path_part)
        )
    if joined == ".." or joined.startswith("../"):
        return ESCAPES, joined
    for submodule in submodules:
        if joined == submodule or joined.startswith(f"{submodule}/"):
            return SUBMODULE, joined
    if (repo_root / joined).exists():
        return RESOLVED, joined
    return MISSING, joined


def _git(repo_root: Path, *args: str) -> str:
    """Run a git query in *repo_root*, with actionable failures."""
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=repo_root,
            capture_output=True,
            text=True,
            check=True,
        )
    except FileNotFoundError as exc:
        raise RuntimeError(
            "git is not on PATH - this check reads the tracked file list"
        ) from exc
    except subprocess.CalledProcessError as exc:
        detail = (exc.stderr or exc.stdout or "").strip()
        raise RuntimeError(f"git {' '.join(args)} failed: {detail}") from exc
    return result.stdout


def tracked_markdown(repo_root: Path) -> list[str]:
    """Return the tracked ``*.md`` files, POSIX-spelled and sorted."""
    entries = _git(repo_root, "ls-files", "-z").split("\0")
    return sorted(entry for entry in entries if entry.lower().endswith(".md"))


def check(repo_root: Path) -> tuple[list[str], list[Link], list[Finding], dict[str, int]]:
    """Scan the tracked Markdown, returning files, links, findings and counts."""
    gitmodules = repo_root / ".gitmodules"
    submodules = (
        submodule_paths(gitmodules.read_text(encoding="utf-8"))
        if gitmodules.is_file()
        else []
    )
    files = tracked_markdown(repo_root)
    links: list[Link] = []
    findings: list[Finding] = []
    counts = {EXTERNAL: 0, ANCHOR: 0, SUBMODULE: 0, RESOLVED: 0}
    for source in files:
        text = (repo_root / source).read_text(encoding="utf-8", errors="replace")
        for link in links_in(text, source):
            links.append(link)
            kind, resolved = classify_target(link.target, source, repo_root, submodules)
            if kind in counts:
                counts[kind] += 1
                continue
            why = (
                "link escapes the repository"
                if kind == ESCAPES
                else "relative link points at nothing"
            )
            findings.append(Finding(link.source, link.line, link.target, why))
    return files, links, findings, counts


def _report(
    files: Sequence[str],
    links: Sequence[Link],
    findings: Sequence[Finding],
    counts: dict[str, int],
) -> None:
    print("Markdown link check")
    print(f"\n  files scanned : {len(files)}")
    print(f"  links found   : {len(links)}")
    print(f"    resolved    : {counts[RESOLVED]}")
    print(f"    external    : {counts[EXTERNAL]} (not fetched)")
    print(f"    anchors     : {counts[ANCHOR]} (not validated)")
    print(f"    submodule   : {counts[SUBMODULE]} (not checked out in CI)")
    if not findings:
        print("\n  OK   every relative link resolves.")
        return
    print("\n  FAIL")
    for finding in findings:
        print(f"    {finding.source}:{finding.line}")
        print(f"      -> {finding.target}")
        print(f"      {finding.why}")
    print(f"\n  {len(findings)} unresolved link(s).")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=REPO_ROOT,
        help="Repository to inspect (default: this file's repository).",
    )
    args = parser.parse_args(argv)

    try:
        files, links, findings, counts = check(args.repo_root)
    except RuntimeError as exc:
        print(f"[link-check] {exc}", file=sys.stderr)
        return 2

    _report(files, links, findings, counts)
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
