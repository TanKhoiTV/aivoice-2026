# Architecture Decision Records — public register

The project's decisions are split by what each one constrains, not by where it
happened to be written.

| Where | Records | Why there |
| --- | --- | --- |
| **Here** (`docs/decisions/`) | ADR-029 licence gate · ADR-030 QAIRT redistribution · ADR-031 Piper GPL split | Licensing is **program layer**: it is a claim about what we may ship, not how we ship it |
| `kavi-android/docs/decisions/` (private) | ADR-001 … ADR-028 | **On-device mechanism**: runtime choice, pipeline, memory budget, thread tuning, conversion workarounds |
| `prototype/docs/decisions/` (public benchmark) | ADR-032 (pending) + the open-parameters register | The **measurement** stays where it was measured |

**The rule both halves follow:** keep the measurement where it was measured, and
keep the decision next to the record it constrains. Where the two disagree, the
public side keeps the claim and the private side the mechanism.

## Public licensing records

| # | Title | Status |
| --- | --- | --- |
| [ADR-029](ADR-029-license-gate.md) | Shipping license gate — adopt/avoid verdicts | **Accepted** — gate in force; one policy fork open (ADR-031) |
| [ADR-030](ADR-030-qairt-runtime-redistribution.md) | QAIRT runtime redistribution is permitted | **Accepted** — resolved 2026-07-19 |
| [ADR-031](ADR-031-piper-engine-gpl-split.md) | Piper engine GPL split | **Proposed** — deferred, not decided |

ADR-029 is the parent record: it decides *which candidates may ship at all*, and
ADR-030/031 resolve two of the forks it left open.

## Where the rest went

- **ADR-001 … ADR-028** — on-device records. They are private because their
  mechanism is (QAIRT toolchain, conversion runbooks, tuning); the public side
  keeps the gates they must satisfy, in `prototype/.kavi.yaml`. Cite them by
  title and repository, never by path: `ADR-020 — pipeline concurrency
  (kavi-android)`.
- **ADR-032 — MT model choice** — public, in `prototype/docs/decisions/`, written
  after the configuration split. Tracked by TanKhoiTV/kavi-benchmark#110. It
  references the on-device records by title + repo, never by number, because the
  private register renumbers independently.
- **`archive/docs/adr/`** — two legacy records from the previous implementation,
  kept verbatim as history. Not part of this register.

## Conventions

- One decision per record; the header carries status (`Proposed` / `Accepted` /
  `Superseded` / `Withdrawn`), date and deciders.
- Records in this directory are immutable once accepted: a change lands as a new
  record that supersedes the old one, and the old header gains the pointer.
- A record that moves repositories keeps its number. The private register does
  not renumber to fill the gap left by these three.
