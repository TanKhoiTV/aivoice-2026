# ADR-031: Piper engine GPL split (closed — moot)

## Status

**Superseded 2026-11-12 — the fork is moot, because Piper is not shipped.**

Was: Proposed — **deferred**, not decided.

## Date

2026-07-15

## Deciders

Project lead

## Context

Piper is a candidate TTS engine. Its licensing is split across two upstreams with
different terms and different maintenance states:

- **`rhasspy/piper`** — MIT, but **frozen and archived** (Oct 2025).
- **`OHF-Voice/piper1-gpl`** — GPL-3.0, actively maintained.

A GPL engine linked into the app would impose copyleft obligations on the whole
binary, which is disqualifying for a commercial closed-source product. So the
choice is not simply "which Piper?", but *whether* the GPL build can be used at
all, and under what isolation.

This fork **shapes all of TTS**, so leaving it undecided is the main route to a
late TTS swap. Note that Piper is no longer the v1 default — see
ADR-009 (v1 TTS: Supertonic — private in `kavi-android`) and
ADR-024 (Piper TTS on CPU — private in `kavi-android`) — which lowers the stakes but does not
remove the fork, since Piper remains the documented fallback.

> **Split note (2026-09-25):** extracted from `license-situation.md` (now
> [ADR-029](ADR-029-license-gate.md)), where it was "fork #1". Unlike the other
> determinations in that record it is **genuinely undecided**, so it is a pending
> decision rather than a resolved verdict.

## Decision

**Deferred — no decision recorded.** The position at the time of writing:

- MIT-era `rhasspy/piper` (frozen, archived Oct 2025) is a **licence-clean
  option** (MIT) and can run via **subprocess isolation**, so the GPL
  `espeak-ng`/engine never links into our binary.
- The GPL build `OHF-Voice/piper1-gpl` (GPL-3.0) is **deferred** — not decided.
- **No tech-stack decision follows from this yet:** Piper (MIT-era) is one TTS
  *option* alongside MeloTTS (MIT) and Kokoro (Apache-2.0); the final pick waits
  for the benchmark harness.

### What would close it

A decision on whether the subprocess-isolation pattern is adopted as the
supported Piper path, or whether Piper is dropped from the shipped stack
entirely in favour of the v1 default.

### How it closed — 2026-11-12

Neither branch of the fork was taken, because **Piper left the shipped stack on functional and
frontend grounds, not on the licence split**. Recorded in `kavi-android`:

- **The frontend was removed upstream.** sherpa-onnx 2.0.1 dropped espeak-ng and `piper-phonemize`
  (k2-fsa/sherpa-onnx#4055, 2026-10-20). A piper model now refuses text outright: *"No frontend
  available. For piper/icefall/inflect/coqui models, provide phoneme_codepoints via
  GenerationConfig at generate time"*. Supplying them means phonemising outside sherpa — and
  `piper-phonemize` is **GPL-3.0**, which is the same copyleft this record was trying to isolate,
  now moved to the *input* side where subprocess isolation does not help.
- **The MIT-era voice does not work.** The staged build loads and then synthesises zero-length audio,
  and the staged `espeak-ng-data` carries no usable `vi` voice.
- **Two engines ship instead**: Supertonic 3 for VI→EN (OpenRAIL-M weights + MIT code) and VieNeu v3
  Turbo for EN→VI (MIT), per ADR-009 and ADR-028.

So: subprocess isolation is **not adopted**, and **neither Piper build is shipped**. The underlying
policy question is answered by default — but by events, not by a verdict. If Piper ever returns with a
licence-clean frontend, this fork reopens with the isolation question intact rather than settled.

Sources, all in `kavi-android`: `docs/reference/tts-engines.md` (frontend removal, zero-length audio,
licence audit of the candidate set), `docs/reference/backlog.md` item 38 ("the Piper fallback: a bug,
and then a broken asset"), `ADR-009`, `ADR-028`.

## Consequences

### Positive

- Deferring costs nothing today: Piper is not the v1 default
  (ADR-009 (v1 TTS: Supertonic — private in `kavi-android`)).

### Negative / risk

- **The question remains unanswered in principle.** Piper is out because it cannot run, not because the
  isolation pattern was evaluated and rejected. A future re-adoption starts from the same fork.
- The MIT-era upstream is archived, so the clean option is frozen: it will not
  receive fixes.
- Subprocess isolation is an architectural commitment (IPC boundary, lifecycle),
  so adopting it is not a one-line change.

## References

- [ADR-029](ADR-029-license-gate.md) — Shipping license gate (parent record)
- ADR-009 (v1 TTS: Supertonic — private in `kavi-android`) — v1 TTS: SupertonicTTS 3 (current default)
- ADR-024 (Piper TTS on CPU — private in `kavi-android`) — Piper TTS stays on CPU (conversion position)
- `docs/reference/phase-4-qnn-plan.md` §3.3 — Piper conversion, deferred
