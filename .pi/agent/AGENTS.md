# AGENTS.md (Project — aivoice-2026 / Kavi)

Project-level instructions supplementing the user-level AGENTS.md
(`/home/dmin/.pi/agent/AGENTS.md`). The user-level conventions for
communication, coding style, web fetch, and version control also apply here.

---

## Contribution Workflow

Two tiers. The orchestrator (this session's assistant) decides which tier a task
requires when assigning it.

### Pre-task (Orchestrator)

Before starting any task, sync main:

```bash
git fetch --all
git checkout main
git pull origin main --rebase
```

---

### Tier 1: Full Workflow

Use for architecture-significant changes, new features, or any task with
trade-offs. Always produces a GitHub Issue.

```
Advisor ──→ Researcher ──→ Planner ──→ Worker ──→ Reviewer ──→ Manual Review
  │            │              │           │            │
  │ Issue      │ Context      │ Plan as   │ Branch +   │ PR review  │
  │ (DoD/AC)   │              │ Issue     │ PR         │ comments   │
  │            │              │ comment   │            │            │
  └────────────┘              └───────────┘            │
       ↑                        ↑                      │
 Blocked ───────── Escalate ────────←────────────────────┘
```

**Step 1a — Advisor**

- Writes a GitHub Issue with: Description, Definition of Done / Acceptance
  Criteria, loose guidelines and instructions.
- Reports any user-level blockage (pending decisions, unknowns, resource
  constraints).

**Step 1b — Researcher**

- Complements the Advisor with additional context (web research, library docs,
  code search).
- Cycles with Advisor until the picture is clear and the Issue is ready.

**Step 2a — Planner**

- With the Issue created, develops a step-by-step plan.
- Writes the proposed approach as a comment on the Issue.

**Step 2b — Worker**

- Creates a new branch following `<type>/<short-description>` (see
  [Branch Naming](#branch-naming)).
- Follows every step of the plan with no deviation until completion.
- **Responsible for pre-commit checks:** lint, format, tests.
- If blocked, reports as a comment on the Issue and delegates back to Planner.
- Planner can adjust the plan or escalate to Step 1.
- On completion, creates a Pull Request with `Closes #<issue>` in the
  description.

**Step 3a — Reviewer**

- Reviews the Pull Request, flags all issues as PR comments.
- If clean, reports as-is.
- If issues found, escalates back to Step 2.

**Step 3b — Manual Review**

- User reviews the changes.
- If ready: user merges, or delegates merge + local branch cleanup to the
  Reviewer or orchestrator.
- GitHub auto-deletes the remote branch on merge.

---

### Tier 2: Simplified Workflow

Use for minor edits with no architectural impact — typo fixes, doc corrections,
trivial refactors.

- Skip Issue creation, Advisor, Researcher, and Planner phases entirely.
- **Worker** creates branch, implements, runs pre-commit checks, creates PR.
- **Reviewer** reviews the PR.
- **User** merges (or delegates merge + cleanup).
- If the task turns out larger than expected, escalate to the full workflow.

---

## Branch Naming

```
<type>/<short-description>
```

Examples:

```
feat/server-streaming
fix/vad-threshold-clamp
docs/contributing-workflow
chore/issue-templates
ci/release-workflow
```

**Types:**

| Type       | When                             |
| ---------- | -------------------------------- |
| `feat`     | New feature or capability        |
| `fix`      | Bug fix                          |
| `refactor` | Code restructuring, no behavior change |
| `docs`     | Documentation-only changes        |
| `test`     | Adding or updating tests          |
| `chore`    | Repo maintenance (config, templates, tooling) |
| `ci`       | CI/CD pipeline and automation     |

---

## Issue & PR Templates

Templates live in the [blues-estimator-project](https://github.com/TanKhoiTV/blues-estimator-project)
reference repo (`.github/` directory).

**Issue templates:**

- **Task creation** — Description, Definition of Done, Proposed Implementation
- **Bug report** — Bug description, reproduction steps, expected behavior

**PR template** — Description (with `Closes #<issue>`), Testing Proof
(`uv run pytest`), Quality Check (`ruff check` + docstrings), optional Visuals.

---

## Escalation Ladder

When any agent hits a blocker it cannot resolve:

```
Worker → Planner → Advisor → Researcher → User
```

Each level escalates up only if the current level cannot unblock. The Planner
adjusts the plan; the Advisor resolves direction/architecture questions; the
Researcher fills knowledge gaps.

---

## Collaborator Incoming Workflow

Both contributors work across both repos (`aivoice-2026` and `kavi-prototype`);
this section covers how to handle **incoming Issues and PRs** created by a
collaborator, regardless of which repo they land in.

### Incoming Issue Assessment

A collaborator creates an Issue using the Task Creation template (Description +
DoD + Proposed Implementation). Our side handles the assessment:

```
Worker ──→ reads Issue, assesses scope, feasibility, conflicts
   │
Reviewer ──→ reviews assessment for blind spots
   │
User ──→ approves response or directs next action
```

- **Worker** reads the Issue, evaluates scope and potential conflicts, considers
  how it fits the current architecture, and posts a summary comment with
  findings.
- **Reviewer** reviews the assessment for blind spots.
- **User** approves the response or gives a different direction.

This uses the **Simplified workflow** — no new Issue or branch needed on our
side.

### Incoming PR Review & Merge

A collaborator pushes a branch and opens a PR. Our side handles review, merge,
and post-merge cleanup:

```
Worker ──→ reviews PR code, fetches the branch locally, runs checks
   │         (lint, format, tests), posts review comments on the PR
   │
Reviewer ──→ reviews Worker's review for missed issues
   │
User ──→ merges the PR
   │
Worker ──→ bumps submodule pointer (if PR was in kavi-prototype):
   │         cd prototype && git fetch origin main && git checkout main
   │         cd .. && git add prototype
   │         git commit -m "chore(prototype): bump for <feature>"
   │         git push
   │
Worker ──→ verifies remote branch was deleted (GitHub does not always auto-
   │         delete; if it persists, delete manually via GitHub UI or CLI)
Reviewer ──→ verifies submodule pointer update and branch cleanup
```

**Pre-commit checks** run locally on the fetched branch — Worker is
responsible for running the same lint/format/tests as in the main workflow.

**Submodule pointer bump** applies only when the PR targets `kavi-prototype`
and changes its `main` history. If the PR is in `aivoice-2026`, no pointer
update is needed.

**Branch cleanup** — GitHub may or may not auto-delete the remote branch after
merge. Always verify. If it persists, delete it manually via GitHub UI or CLI:

```bash
git push origin -d <branch-name>
```

This uses the **Simplified workflow** — the work is mechanical review and
cleanup, not architectural.
