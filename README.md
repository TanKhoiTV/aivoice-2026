# aivoice-2026 (Kavi)

Umbrella repository for **Kavi**, our entry to the
[OneVoice AI Challenge](https://saigonaihub.com/OneVoiceAIChallenge) — an
offline, on-device speech-to-speech translator for Vietnamese ↔ English.

## This repo is just a shell

All code and documentation live in the **`prototype/` submodule**
([`kavi-prototype`](https://github.com/TanKhoiTV/kavi-prototype)). This parent
repo exists only to tie the project together and host this top-level README.

➡️ **Start here:** [`prototype/README.md`](prototype/README.md)

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
| `prototype/` | The actual project (code + docs) — a git submodule |
| `.gitmodules` | Submodule definition |
