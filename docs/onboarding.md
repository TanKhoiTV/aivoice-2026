# Onboarding to Kavi (aivoice-2026)

> A guide for new team members. It decodes the acronyms, the program's three
> foundational decisions (ADR-001 / 002 / 003), and where each part of the
> project now lives — so you can read the rest of the docs without a translator.
> Pair this with `README.md` (the landing page) and `docs/specifications.md`
> (our targets).

## Start here — reading order (from zero to productive)

You are in the **public program repo** (`aivoice-2026`). It holds the story, the
contest material and this guide. The **host-side benchmark** lives in the
`prototype/` submodule (`kavi-prototype`, also public); the **on-device app** and
most of its ADR register live in the private `kavi-android` repo. Read in this
order — each step builds the mental model you need for the next.

```text
aivoice-2026/                 (PUBLIC program layer — what we tell the world)
├─ README.md                  ①  landing page
├─ docs/
│  ├─ contest-info.md         ②  the contest + how we're graded
│  ├─ specifications.md       ③  our concrete targets + glossary
│  ├─ onboarding.md           ⑥  this file — architecture, decoded
│  ├─ onboarding-quiz.md      —  comprehension checkpoint
│  ├─ decisions/              ⑪  public licensing records (ADR-029–031)
│  └─ reference/
│     └─ additional-reading.md  ⑫  the self-study syllabus
├─ archive/                   —  the previous implementation, reference only
└─ prototype/                 (submodule: kavi-prototype, PUBLIC benchmark)
   ├─ README.md               ④  harness + how to run
   ├─ CONTRIBUTING.md         ⑤  cloning + tooling
   ├─ docs/benchmark/         —  the published v1 results + report
   ├─ docs/reference/         ⑬  benchmarking plan, denoising gate, corpus catalog
   └─ bench/                  —  the harness (candidates, scorer, data prep)

kavi-android/                 (PRIVATE on-device track)
├─ kavi-tuning.yaml           —  build + runtime tuning
├─ docs/decisions/           ⑩  the ADR register (start at its README)
│  ├─ ADR-001 …              ⑦  100% offline, forever
│  ├─ ADR-002 …              ⑧  one phone: Snapdragon 8 Gen 2
│  ├─ ADR-003 …              ⑨  CPU now, NPU later
│  ├─ ADR-005 …              ⑭  QNN conversion workarounds
│  └─ ADR-006 …              ⑮  Android runner architecture
└─ docs/                     —  implementation plans, NDK/QAIRT runbook
```

**What to conclude from each:**

1. **This repo's `README.md`** → the public landing page; the story, the layout,
   and the checks that keep the three repositories honest.
2. **`docs/contest-info.md`** → Kavi is an entry to the **OneVoice AI Challenge**
   (Saigon AI Hub × Qualcomm, May–Nov 2026); an offline VI↔EN speech-to-speech
   translator; here are the contest rules + the six grading metrics.
3. **`docs/specifications.md`** → our translated targets — offline, RTF < 1.0,
   turnaround < 2.0 s, BLEU/COMET both ways, TTS MOS, stability — plus a newcomer
   acronym glossary. This is the scoreboard "good" is measured against.
4. **Submodule `README.md`** (`prototype/README.md`) → the host-side harness:
   candidates, scorer, how to build the eval set and run it.
5. **Submodule `CONTRIBUTING.md`** (`prototype/CONTRIBUTING.md`) → clone with
   `--recurse-submodules`; a plain parent clone skips the benchmark. Then
   `make setup` for deps + pinned models/data. Tooling: ruff + commitlint +
   pre-commit.
6. **`docs/onboarding.md`** (this file) → plain-language walkthrough of the three
   architecture decisions, so the ADRs below make sense without prior context.
7. **`ADR-001` (offline-first, private)** → **zero cloud, ever.** A network call
   during testing is an instant disqualification.
8. **`ADR-002` (target platform, private)** → we optimize for **one device** —
   Snapdragon 8 Gen 2, Android 16, Hexagon HTP v73. Phone-only.
9. **`ADR-003` (Hexagon runtime, private)** → start on **CPU (ORT-XNNPACK int8)** —
   license-clean, ships today; add **NPU / QAIRT later** after on-device
   benchmarks. NNAPI rejected.
10. **The ADR register** (private: `kavi-android/docs/decisions/README.md`) →
    **one decision per record.** Start there rather than reading ADRs in number
    order: it lists every record with its status, the supersession graph, and the
    parameters still open. The tech-stack choices are spread across records —
    ADR-007 (service) with ADR-013–022 (pipeline), ADR-008 (Dual Zipformer ASR,
    CPU-only per ADR-027), ADR-009 (Supertonic Phase-1 TTS), ADR-010 (`ALL_OPT`).
    **ADR-004 is withdrawn** — it was the deferred tech-stack register, which the
    index has replaced. The on-device records are private because their mechanism
    is; the public side keeps the claim it constrains.
11. **`docs/decisions/ADR-029-license-gate.md`** → most candidates are license-clean;
    this gate is *why* we can pick safely. TTS licensing is **resolved for v1**
    (ADR-009: Supertonic); the **Piper GPL split** matters only if the fallback is
    exercised — pin the MIT-era `rhasspy/piper` snapshot then. ADR-030 (QAIRT
    redistribution) and ADR-031 (Piper GPL split) sit beside it: licensing is
    program layer, so all three records are public here.
12. **Submodule `docs/reference/benchmarking-plan.md`** → we **benchmark before choosing** — datasets,
    the ASR/MT/TTS candidate landscape, the pluggable harness design, the lean v0.
13. **Submodule `docs/reference/benchmarking-todo.md`** → the **execution checklist** (phases 0–7,
    checkboxes) to produce those numbers — what you'd actually pick up and work on.
14. **`ADR-005` (QNN conversion workarounds, private)** → when the QAIRT converter
    rejected ops (`IsNaN`, cyclic graphs), these are the workarounds: strip `IsNaN`
    from the decoder (ADR-005), run decoders on CPU (ADR-023), keep TTS on CPU
    (ADR-024).
15. **`ADR-006` (Android runner architecture, private)** → native on-device instrumented
    test (no ADB bridge), single push/pull, internal timing, zero-network
    assertion; with the fixed-shape padding rule in ADR-025 and real-data-only
    calibration in ADR-026.

> **Skip for now:** `archive/` (historical, superseded) and
> `prototype/docs/README.md` (the benchmark docs index).

## What Kavi is, in one breath

Kavi is an entry to the **OneVoice AI Challenge** (Saigon AI Hub × Qualcomm,
May–Nov 2026): a **real-time speech-to-speech translator** for **Vietnamese ↔
English** (later Chinese, Korean) that runs **entirely on a phone**, with **no
internet**. It is built for workers in **factories, construction sites, and
logistics hubs** — noisy, hands-busy, low-connectivity places where cloud
translation fails.

The pipeline is a single local chain:

```text
[mic] → VAD → denoise → ASR → MT → TTS → [speaker]
```

- **VAD** — Voice Activity Detection (find the speech, skip silence)
- **denoise** — strip industrial noise while keeping Vietnamese tone
- **ASR** — Automatic Speech Recognition (speech → text)
- **MT** — Machine Translation (text → text, VI↔EN)
- **TTS** — Text-to-Speech (text → spoken output)

Everything between the microphone and the speaker happens on-device.

## The three decisions you must know

These are the **Architecture Decision Records (ADRs)** in the private
`kavi-android/docs/decisions/`. Read them as "here is what we locked in, and
why." They are the backbone of everything else. The licensing trio
(ADR-029–031) is public in this repo, under `docs/decisions/`.

### ADR-001 — Offline-first, on-device (Accepted)

**Plain version:** Kavi runs 100% on the phone. No cloud, no network calls,
ever, while it is translating.

**Why:** the contest **disqualifies** any entry that touches the network during
testing. Separately, the actual users (factory floors) often have no reliable
connection — so offline is the product, not a fallback.

**What it forces:** every model must be small enough to run on the phone
**within ~2 seconds** end-to-end (turnaround < 2.0 s) and keep pace with live
speech (RTF < 1.0). It also means **no runtime telemetry** — analytics, if any,
are queued locally.

### ADR-002 — Target platform: Snapdragon 8 Gen 2, Android 16, Hexagon NPU (Accepted)

**Plain version:** we build and test for **one specific phone configuration**:
a **Snapdragon 8 Gen 2** running **Android 16**, using its **Hexagon NPU** (the
AI chip) as the primary compute, with **GPU → CPU** as fallback.

**Why:** Qualcomm co-hosts the contest and offers **Qualcomm AI Hub** — models
pre-optimized for Snapdragon. A phone is the required portable form factor.
Wearables / headsets are out of scope.

**What it forces:** models are compiled for that NPU generation (**HTP v73**);
benchmarks run on **real hardware** (emulators don't exercise the NPU); newer
Snapdragon 8 parts *may* work but aren't guaranteed.

### ADR-003 — Hexagon runtime strategy (Proposed — not final yet)

**Plain version:** the plan for *how* we reach that NPU is to use Qualcomm's
**QAIRT / QNN** runtime (via ONNX Runtime), with models **quantized**
(compressed to low-precision numbers) and **fixed input sizes**, falling back
to CPU if the NPU path isn't ready.

**Why provisional:** we haven't benchmarked on the real phone yet, so this ADR
will be amended once numbers exist.

**The catch that matters most:** our *current v0 harness* runs ASR via
**faster-whisper** (CTranslate2-backed) and MT via **CTranslate2** — and **neither
can be converted to QNN**. QNN only ingests PyTorch / TFLite / ONNX. So getting NPU speed likely
means **re-sourcing models in a convertible format** (e.g. Opus-MT → ONNX →
QAIRT). **NNAPI is explicitly avoided** (deprecated in Android 15; we target
16). The safe path is **CPU-first**, then layer NPU.

## Glossary — decode the cryptic

| Term | Plain meaning | Why it matters here |
| --- | --- | --- |
| **S2ST / S2S** | Speech-to-speech translation | What Kavi *is*. |
| **VI↔EN** | Vietnamese ↔ English | Our language pair (later ZH, KO). |
| **ADR** | Architecture Decision Record | A written, durable "we chose X because Y". In `kavi-android/docs/decisions/` (ADR-001–028) or `docs/decisions/` here (ADR-029–031, licensing). |
| **SoC** | System-on-Chip | The whole phone computer on one chip (CPU + GPU + NPU). |
| **NPU** | Neural Processing Unit | The chip's AI accelerator; far faster / power-efficient than CPU for models. |
| **Hexagon** | Qualcomm's NPU brand | Our NPU. |
| **HTP v73** | Hexagon Tensor Processor, version 73 | The 8 Gen 2's NPU generation. Compiled models are version-locked to it (8 Gen 3 = v75, 8 Elite = v79 / v81). |
| **QNN / QAIRT** | Qualcomm Neural Network / Qualcomm AI Runtime SDK (QNN rebranded at v2.32) | The runtime / compiler that runs models on Hexagon. Our planned primary path. |
| **ONNX** | Open Neural Network Exchange | A common, tool-agnostic model format. The lingua franca for conversion. |
| **ORT** | ONNX Runtime | The inference engine; talks to NPU / CPU / GPU via "Execution Providers". |
| **EP (Execution Provider)** | ORT's backend plugin | e.g. QNN EP (NPU), OpenCL EP (GPU), XNNPACK (CPU int8). |
| **HTP v73 context binary** | Qualcomm's compiled model format | The output of `qnn-context-binary-generator --htp_arch v73`. Device-specific; not portable across SDK versions or hardware targets. |
| **AI Hub** | Qualcomm's model catalog + device farm | Free, build-time only; gives pre-optimized models and remote test devices. |
| **AIMET** | AI Model Efficiency Toolkit | Qualcomm tool for quantization, run on a PC (x86_64). |
| **int8 / w8a16** | 8-bit integer weights / 8-bit weights + 16-bit activations | The low-precision formats the NPU needs; w8a16 protects accuracy. |
| **NNAPI** | Android Neural Networks API | Avoided — deprecated in Android 15; we target 16. |
| **RTF** | Real-Time Factor | processing time ÷ audio time. **< 1.0** = faster than real-time (required). |
| **WER / CER** | Word / Character Error Rate | ASR accuracy (lower is better). |
| **BLEU / COMET** | MT quality metrics | Translation accuracy (higher is better). |
| **MOS** | Mean Opinion Score | Human-rated TTS naturalness (1–5). |
| **TTFT** | Time To First Token | Latency to first output from a streaming model. |
| **EOS→SA** | End Of Speech → Start of Audio | The < 2.0 s turnaround we must hit. |
| **VAD** | Voice Activity Detection | Finds speech, drops silence. |
| **CT2 / CTranslate2** | CPU MT runtime we currently use | Fast on CPU, but **not QNN-convertible**. |
| **faster-whisper / whisper.cpp** | Current v0 ASR runtime (faster-whisper, CTranslate2-backed) / alternative (whisper.cpp) | Same problem — **neither is QNN-convertible**; NPU needs re-sourcing. |
| **DQ** | Disqualification | What a network call during testing causes. |

## Repository layout — what lives where

This repo is the **program layer**; the previous implementation is preserved
under `archive/` for reference.

| Path | What it is |
| --- | --- |
| `docs/` | Public program docs — contest brief, specification, this guide, the quiz, the reading list. |
| `docs/decisions/` | The public licensing records (`ADR-029`, `ADR-030`, `ADR-031`). |
| `archive/` | The old implementation (old `pipeline.py`, `architecture.md`, `design.md`, legacy ADRs, experiments). **Reference only — do not edit.** |
| `prototype/` | Git submodule: `kavi-prototype`, the public host-side benchmark — harness, eval sets, `docs/benchmark/` results and the Typst report. |
| `scripts/`, `tests/` | The public-boundary and Markdown-link checks, plus their unit tests. |
| `.github/` | CI for those checks, and `CODEOWNERS`. |

Two things are **not** here, by design:

- **The on-device app** — private, in `kavi-android`: app code, `kavi-tuning.yaml`,
  the on-device ADR register (ADR-001–028), the QAIRT/NDK conversion toolchain.
- **The harness itself** — public, in the `prototype/` submodule: `bench/`,
  `docs/benchmark/`, eval-set preparation, the model and dataset pins.

## The model-licensing rule (contest-critical)

The contest can lead to **commercialization**, so every model must permit
commercial use. This single rule eliminates several otherwise-attractive models.
Full detail is in `prototype/docs/reference/benchmarking-plan.md` §4.4–§4.5.

- **Commercial-clean (use these):** Opus-MT (Apache-2.0), MeloTTS (MIT),
  MADLAD-400 (Apache-2.0), M2M-100 (MIT), Kokoro (Apache-2.0),
  vietTTS / VITS (MIT / Apache, verify InfoRe terms), SpeechT5 (MIT).
- **TTS — resolved for v1 (ADR-009):** Supertonic Phase 1 → VieNeu-TTS Phase 2,
  via sherpa-onnx; Piper VITS is fallback only. The old MIT/GPL fork question
  matters only if the fallback is exercised (pin the MIT-era `rhasspy/piper`
  snapshot then). See `prototype/docs/reference/benchmarking-plan.md` §4.5 for the landscape.
- **Avoid (license blocks):** **NLLB** (CC-BY-NC), **MMS-TTS-vie** (CC-BY-NC),
  **Coqui XTTS** (CPML — restrictive; Coqui Inc. shut down Jan 2024).
- **Caution (verify):** **Hy-MT** (HY Community License — commercial-permitted
  *per old ADR-001*, but a regional carve-out is flagged by our current stance).

## Where the architecture is going

The **tech stack is decided** across several records: ADR-007 (service) with
ADR-013–022 (pipeline), ADR-008 (Dual Zipformer ASR, CPU-only per ADR-027),
ADR-009 (Supertonic Phase-1 TTS), ADR-010 (`ALL_OPT`). **ADR-004 is withdrawn** —
the parameter table it maintained is now the
[open-parameters register](../prototype/docs/decisions/README.md#open-parameters),
which closes as the Phase-4/5/7 on-device numbers and hard gates land. The
register is public; the on-device records it tracks are private, and the public
side keeps the claim each one constrains.

## How to get running & next steps

1. **Clone** (see `CONTRIBUTING.md` → Cloning):

   ```bash
   git clone --recurse-submodules git@github.com:TanKhoiTV/aivoice-2026.git
   cd aivoice-2026/prototype && git checkout main
   ```

2. **Bootstrap & check** — the harness commands run inside the submodule
   (`make setup` fetches the pinned model weights and FLEURS data; `make setup-min`
   is the offline path):

   ```bash
   cd prototype
   make setup
   make check
   make test
   ```

3. **Read in order** — see **Start here** (top of this guide): this repo's
   `README.md` → `contest-info.md` → `specifications.md`, then the submodule docs
   (`README.md` → `docs/reference/benchmarking-plan.md`). The on-device records are
   private; ask for access before relying on them.
4. **The v0 harness is built** (`bench/`) — build the eval set and run it:

   ```bash
   make models       # pinned Opus-MT weights (already fetched by `make setup`)
   make bench-data   # -> eval_data/eval_manifest_v1.json
   make bench        # run the harness (offline smoke: Opus-MT vi->en + Piper EN TTS)
   make test         # run the pytest suite
   ```

   Feed the numbers into the [open-parameters register](../prototype/docs/decisions/README.md#open-parameters).

> **If you remember nothing else:** Kavi is a fully-offline phone translator
> (VI↔EN); we target **one chip** (Snapdragon 8 Gen 2 / Hexagon HTP v73); the
> runtime path is **QAIRT / QNN via ONNX Runtime, CPU-first**; models must be
> **commercial-licensed** and **small enough for < 2 s**; and the **exact model
> choices are still TBD** behind the open-parameters register + the benchmark harness.
