"""Tests for the Markdown link check (``scripts/link_check.py``)."""

from __future__ import annotations

import contextlib
import io
import tempfile
import unittest
from pathlib import Path

from scripts.link_check import (
    ANCHOR,
    ESCAPES,
    EXTERNAL,
    MISSING,
    REPO_ROOT,
    RESOLVED,
    SUBMODULE,
    check,
    classify_target,
    links_in,
    main,
    submodule_paths,
)


class TestLinksIn(unittest.TestCase):
    """Extraction: what counts as a link, and where."""

    def test_inline_link_and_line_number(self) -> None:
        text = "# Title\n\nSee [the docs](docs/).\n"
        self.assertEqual(links_in(text, "README.md")[0].target, "docs/")
        self.assertEqual(links_in(text, "README.md")[0].line, 3)

    def test_image_is_a_link(self) -> None:
        (link,) = links_in("![diagram](assets/diagram.png)\n", "README.md")
        self.assertEqual(link.target, "assets/diagram.png")

    def test_reference_definition(self) -> None:
        (link,) = links_in("[spec]: docs/specifications.md\n", "README.md")
        self.assertEqual(link.target, "docs/specifications.md")

    def test_title_is_not_part_of_the_target(self) -> None:
        (link,) = links_in('[spec](docs/spec.md "Spec")\n', "README.md")
        self.assertEqual(link.target, "docs/spec.md")

    def test_fenced_code_is_ignored(self) -> None:
        text = "```bash\ngit clone [not a link](nope.md)\n```\n"
        self.assertEqual(links_in(text, "README.md"), [])

    def test_links_after_a_fence_are_found_again(self) -> None:
        text = "```\n[x](nope.md)\n```\n\n[real](README.md)\n"
        (link,) = links_in(text, "README.md")
        self.assertEqual(link.target, "README.md")


class TestSubmodulePaths(unittest.TestCase):
    """Submodule detection comes from ``.gitmodules``."""

    def test_path_is_parsed(self) -> None:
        text = (
            "# comment\n"
            '[submodule "prototype"]\n'
            "\tpath = prototype\n"
            "\turl = git@github.com:TanKhoiTV/kavi-prototype.git\n"
        )
        self.assertEqual(submodule_paths(text), ["prototype"])

    def test_no_sections(self) -> None:
        self.assertEqual(submodule_paths("# no submodules\n"), [])


class TestClassifyTarget(unittest.TestCase):
    """Resolution: what each kind of target points at."""

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self._tmp.name)
        (self.repo / "docs").mkdir()
        (self.repo / "docs" / "contest-info.md").write_text("x", encoding="utf-8")
        (self.repo / "docs" / "two words.md").write_text("x", encoding="utf-8")
        (self.repo / "README.md").write_text("x", encoding="utf-8")
        self.addCleanup(self._tmp.cleanup)
        self.submodules = ["prototype"]

    def resolve(self, target: str, source: str = "README.md") -> tuple[str, str]:
        return classify_target(target, source, self.repo, self.submodules)

    def test_absolute_url_is_external(self) -> None:
        self.assertEqual(self.resolve("https://example.com/x")[0], EXTERNAL)
        self.assertEqual(self.resolve("mailto:someone@example.com")[0], EXTERNAL)

    def test_bare_anchor_is_not_resolved(self) -> None:
        self.assertEqual(self.resolve("#section")[0], ANCHOR)

    def test_relative_file_from_the_root(self) -> None:
        self.assertEqual(self.resolve("docs/contest-info.md"), (RESOLVED, "docs/contest-info.md"))

    def test_relative_file_from_a_subdirectory(self) -> None:
        self.assertEqual(
            self.resolve("contest-info.md", "docs/specifications.md"),
            (RESOLVED, "docs/contest-info.md"),
        )

    def test_directory_link(self) -> None:
        self.assertEqual(self.resolve("docs/"), (RESOLVED, "docs"))

    def test_leading_slash_is_repository_relative(self) -> None:
        self.assertEqual(self.resolve("/docs/contest-info.md")[0], RESOLVED)

    def test_percent_encoding_is_decoded(self) -> None:
        self.assertEqual(self.resolve("docs/two%20words.md")[0], RESOLVED)

    def test_parent_traversal_inside_the_repo_is_fine(self) -> None:
        self.assertEqual(
            self.resolve("../README.md", "docs/specifications.md"), (RESOLVED, "README.md")
        )

    def test_fragment_is_stripped(self) -> None:
        self.assertEqual(self.resolve("docs/contest-info.md#4")[0], RESOLVED)

    def test_missing_target(self) -> None:
        self.assertEqual(self.resolve("docs/does-not-exist.md")[0], MISSING)

    def test_leaving_the_repository_is_a_finding(self) -> None:
        self.assertEqual(self.resolve("../outside.md")[0], ESCAPES)

    def test_submodule_targets_are_skipped(self) -> None:
        self.assertEqual(self.resolve("prototype/README.md"), (SUBMODULE, "prototype/README.md"))


class TestThisRepository(unittest.TestCase):
    """What CI enforces on the real docs."""

    def test_every_relative_link_resolves(self) -> None:
        _, _, findings, _ = check(REPO_ROOT)
        self.assertEqual(findings, [], f"unresolved links: {findings}")

    def test_the_readme_submodule_link_is_the_only_skipped_one(self) -> None:
        files, links, _, counts = check(REPO_ROOT)
        self.assertIn("README.md", files)
        self.assertGreaterEqual(len(links), 5)
        self.assertEqual(counts[SUBMODULE], 1)
        self.assertGreaterEqual(counts[EXTERNAL], 1)


class TestMain(unittest.TestCase):
    """CLI behaviour."""

    def test_clean_repository_exits_zero_with_ascii_output(self) -> None:
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = main([])
        self.assertEqual(code, 0, out.getvalue())
        self.assertIn("OK", out.getvalue())
        self.assertTrue(out.getvalue().isascii())


if __name__ == "__main__":
    unittest.main()
