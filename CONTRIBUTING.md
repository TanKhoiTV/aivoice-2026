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

The submodule uses a relative URL (`../aivoice-2026-prototype.git`) pointing
to a local bare repo. Git's file transport is restricted by default; enable it:

```bash
git config protocol.file.allow always
```

When a GitHub remote is created later, update `.gitmodules` to use the
public URL and `git submodule sync` to propagate.
