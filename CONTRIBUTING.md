# Contributing

## Versioning

This project uses **Semantic Versioning** (`MAJOR.MINOR.PATCH`).
Breaking changes increment the MAJOR version; backwards-compatible
features increment MINOR; patches and bugfixes increment PATCH.

## Commit Convention

All commits must follow **Conventional Commits**:

```
<type>(<scope>): <description>
```

**Types:** `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `perf`, `style`

**Scope:** optional; use `prototype`, `eval`, `docs`, `pitch`, `adr`, etc.

**Breaking changes:** append `!` after the type:

```
feat!: restructure pipeline config
```

## Submodules

The `prototype/` directory is a **git submodule**. After cloning:

```bash
git clone --recurse-submodules <repo-url>
# or, if already cloned:
git submodule update --init
```

## Local Development Setup

Both repos are **private** — ask a maintainer to add you as a collaborator
before proceeding.

Clone the project with submodules using the SSH URL:

```bash
git clone --recurse-submodules git@github.com:TanKhoiTV/aivoice-2026.git
```

If already cloned, initialize the submodule separately:

```bash
git submodule update --init
```

The submodule URL (`git@github.com:TanKhoiTV/kavi-prototype.git`) is already
configured in `.gitmodules`. No local bare repo or `protocol.file.allow` is
needed.

Set up the development environment:

```bash
uv sync
```

Verify everything is working:

```bash
make check
```
