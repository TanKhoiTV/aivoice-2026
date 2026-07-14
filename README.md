# aivoice-2026 (Kavi)

Umbrella repository for **Kavi**, our entry to the
[OneVoice AI Challenge](https://saigonaihub.com/OneVoiceAIChallenge) — an
offline, on-device speech-to-speech translator for Vietnamese ↔ English.

## This repo is just a shell

This parent repo is **public**; the real implementation (code + internal
documentation) lives in the **private** `prototype/` submodule
([`kavi-prototype`](https://github.com/TanKhoiTV/kavi-prototype)). This repo hosts
the project's public-facing documentation and links into the private codebase.

➡️ **Start here:** [`prototype/README.md`](prototype/README.md)

## Documentation

Public project documentation (contest rules, registration, pitch) lives in
[`docs/`](docs/):

- [OneVoice AI Challenge — Contest Information](docs/contest-info.md)
- [Technical Specifications & Grading](docs/specifications.md)

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
