# aivoice-2026 (Kavi)

Umbrella repository for **Kavi**, our entry to the
[OneVoice AI Challenge](https://saigonaihub.com/OneVoiceAIChallenge) — an
offline, on-device speech-to-speech translator for Vietnamese ↔ English.

## This repo is just a shell

This parent repo hosts the project's public-facing documentation. The real
implementation (code + internal documentation) lives in the `prototype/`
submodule ([`kavi-prototype`](https://github.com/TanKhoiTV/kavi-prototype)).

> The Android application lives in a separate private repository and is not
> publicly available.

➡️ **Start here:** [`prototype/README.md`](prototype/README.md)

## Documentation

Public project documentation (contest rules, specifications) lives in
[`docs/`](docs/):

- [OneVoice AI Challenge — Contest Information](docs/contest-info.md)
- [Technical Specifications & Grading](docs/specifications.md)

## Repository checks

CI runs three checks on every push and pull request
([`.github/workflows/docs.yml`](.github/workflows/docs.yml)). They are
stdlib-only, so the same commands work locally with no setup:

```bash
python3 scripts/leak_check.py --allow-gitlink prototype   # public boundary
python3 scripts/link_check.py                             # relative links resolve
python3 -m unittest discover -s tests                     # unit tests for both
```

- **Public boundary** (`scripts/leak_check.py`) — the on-device Android track is
  private, so private-track artifacts must not be tracked in either public repo:
  native QNN libraries, Gradle/Android files, app sources, model weights,
  keystores, and machine-local config. `--allow-gitlink prototype` is the one
  permitted exception, because this repo tracks the *public* benchmark as a
  submodule; any other gitlink is a finding.
- **Markdown links** (`scripts/link_check.py`) — moving documentation between the
  three repositories is exactly when relative links break and nothing notices.
  Links into the `prototype/` submodule are skipped (CI does not check it out)
  and external URLs are counted but never fetched, so the check stays offline and
  deterministic.

## Cloning

```bash
git clone --recurse-submodules git@github.com:TanKhoiTV/aivoice-2026.git
cd aivoice-2026/prototype
uv sync
make test
```

If you already cloned without `--recurse-submodules`:

```bash
git submodule update --init
```

## Layout

| Path | What it is |
| ------ | ------------ |
| `docs/` | Public-facing project documentation (contest, specs) |
| `prototype/` | The actual implementation (code + internal docs) — a git submodule |
| `.gitmodules` | Submodule definition |
