# Registration Checklist — OneVoice AI Challenge

> **Deadline:** June 24, 2026 (Luma)  
> **Drop-dead target:** Submit by June 22 for buffer  
> **Last updated:** 2026-06-13 (2026-06-14 update: admin decisions, risk assessment)

---

## 🔴 Must-Have (registration won't submit without these)

| # | Item | Est. time | Owner | Done? |
|---|------|-----------|-------|:-----:|
| 1 | **Decide: Individual or Team?** | ✅ Done | | ✅ → **Team of 2** |
| 2 | **Pick a project name** | 30 min | | ☐ → Still undecided |
| 3 | **Fill Google Sheets template** | 1 hr | Me (lead) | ☐ |
| 4 | **Draft Luma form long answers** | 3 hrs | Me (lead) | ☐ |
| 5 | **Create a pitch deck (PDF)** | 4–6 hrs | | ☐ |
| 6 | **Set up GitHub repo with scaffold** | 2 hrs | | ☐ |
| 7 | **Fill Luma form + submit** | 1 hr | Me (lead) | ☐ |

### Details

**1. Applicant type**
- ✅ **Team of 2** — user (lead/sign-up) + 1 teammate
- Google Sheets template: Part 3+4 (Team info + Member table)
- Luma form: user's email/phone on the account

**2. Project name**
- ❌ Still undecided, needs team discussion
- Needs to be memorable, relevant to speech translation, available on GitHub.

**3. Google Sheets template**
- Link: https://docs.google.com/spreadsheets/d/1L4lc7vOiovBdRgDQ3Xmw3hADomxThHa1zE_Lfi8TlvQ
- Fill in: Applicant Type → Personal/Team Info → Team Member Table
- Set sharing to "Anyone with the link can view"
- Paste the link into the Luma form

**4. Luma form long-answer fields** (source content in `docs/architecture.md`)

| Field | Source | Notes |
|-------|--------|-------|
| Name of your project | Needs decision (#2) | |
| Briefly describe your proposed solution | §4.1 Pipeline + §3.2 Framing | Synthesize into 3-4 sentences |
| What makes it innovative or different? | §6 Innovation Anchors + §7.2 Differentiation Matrix | Lead with MeloTTS-VI Hub + DeepFilterNet |
| Describe your technical approach | §4 Architecture + §5 Components | Pipeline diagram + each stage + device |
| Expected language pair | §4.2 — VI↔EN only | Single-select dropdown |
| Project's current development phase | — | Pre-prototype, architecture phase |
| Real-world use case or industry | §3.2 + §1 Problem Statement | Factories, construction, logistics |
| What impact do you expect? | §1 statistics (5%/87%) | Synthesize into a narrative |
| How could it evolve into a product? | §3.4 Business Viability strategy | Snapdragon-first, zero hardware cost |

**5. Pitch deck**
- 8–10 slides: Problem → Solution → Architecture → Innovation → Pipeline → Team → Timeline
- PDF format preferred per form
- Can reuse diagrams from `docs/architecture.md`

**6. GitHub repo**
- Initialize with README (architecture overview + pipeline diagram)
- Scaffold directory structure (vad/, asr/, mt/, tts/, utils/)
- Push to remote (GitHub)
- Link in the Luma form

---

## 🟡 Should-Have (competitive differentiation at registration)

| # | Item | Est. time | Owner | Done? |
|---|------|-----------|-------|:-----:|
| 8 | **Run DeepFilterNet WER experiment** | ~2 days | | ☐ |
| 9 | **Push pipeline scaffolding code** | 3–4 hrs | | ☐ |
| 10 | **Wire up basic ASR→MT→TTS chain on laptop** | 1–2 days | | ☐ |

### Details

**8. DeepFilterNet WER experiment**
- CPU-runnable (ONNX). Compare: (a) no denoising, (b) RNNoise/WebRTC NS, (c) DeepFilterNet
- Dataset: VIVOS + synthetic 65dB SPL industrial noise
- Even partial results (one condition pair) beat "we hypothesize"
- ⚠️ **Moderate risk** — not a guaranteed win

**Why it might not pay off:**

| Not a technical failure | An actual failure |
|------------------------|-------------------|
| Null result (all 3 within ±2% WER) — Whisper is already robust at moderate noise levels | Dependencies don't work on dev machine (~10% risk) |
| DeepFilterNet hurts WER — treats Vietnamese tonal F0 as noise and suppresses it (~20% risk) | (Rare with ONNX — prior art confirms it runs) |

**Verdict:** Worth running — even null/negative results are still evidence you can cite for a competition with 50% Technical weight. But don't *bank* on a glowing result for the pitch deck. Have the story ready for all three outcomes. Quick environment smoke-test first: does DeepFilterNet ONNX even load on your machine?

**Item 9** (pipeline scaffolding): Near-zero risk. Directory structure + stubs + wrapper functions around well-known libraries. Only failure mode is scope creep.

**Item 10** (basic ASR→MT→TTS chain): Low risk. Components are mature. Main friction point is dependency versioning (PyTorch + transformers combo). 80-90% chance of getting one sentence through on CPU.

**9. Pipeline scaffolding code**
- Silero VAD integration stub
- Whisper inference stub (faster-whisper)
- Hy-MT1.5 wrapper stub (Tencent HY-MT inference via STQ kernel)
- MeloTTS stub
- Shows architecture thinking even before functional integration

**10. Basic end-to-end demo**
- Get ONE sentence through Whisper → translation → MeloTTS on CPU
- Record a screen capture = demo video for the form
- Latency will be terrible on CPU, but the *fact of working* matters more

---

## 🔵 Nice-to-Have (bonus, fill time permitting)

| # | Item | Est. time | Owner | Done? |
|---|------|-----------|-------|:-----:|
| 11 | **Record a 60-second prototype demo** | 2 hrs | | ☐ |
| 12 | **MOS pre-test for MeloTTS-VI plan** | 1 day | | ☐ |
| 13 | **Team page / LinkedIn profiles** | 30 min | | ☐ |

---

## 📋 Admin / Decisions

| # | Decision | Status |
|---|----------|:------:|
| A | Solo or team? | ✅ **Team of 2** — user (lead/sign-up) + 1 teammate |
| B | Project name | ❌ Undecided — needs team discussion |
| C | Who submits the form? | ✅ **User** (lead) — email/phone on the account |
| D | Testing device | ✅ **SD8G2 phone available** — dev on laptop, profile/test on phone |
| E | Pitch deck style (technical vs investor-facing) | ❌ Undecided — needs team discussion |
| F | Expected language pair | ✅ **VI↔EN only** (single-select on Luma form) |

---

## 🏃 Suggested Sprint

| Day | Focus |
|-----|-------|
| **Day 1** (Jun 13) | Decisions (team, project name) + GitHub setup + Google Sheets template |
| **Day 2** (Jun 14 — today) | Pitch deck style decision + DeepFilterNet smoke test + Luma answers outline |
| **Day 3** (Jun 15) | Pitch deck draft + DeepFilterNet WER experiment running |
| **Day 4** (Jun 16) | Code scaffolding (pipeline stubs) + finalize Luma answers |
| **Day 5** (Jun 17) | Review + polish everything + basic chain try |
| **Day 6** (Jun 18) | 🚀 **Submit early** — free up focus for Phase 2 |
| **Buffer** (Jun 19–24) | Only if artifacts aren't ready yet |

---

## Tech Research Findings (2026-06-13)

### TTS Layer — MeloTTS-VI Community Checkpoint Exists

A pre-trained Vietnamese MeloTTS checkpoint already exists and can save months of work:
- **Checkpoint:** [nmcuong/MeloTTS-Vietnamese](https://huggingface.co/nmcuong/MeloTTS-Vietnamese) on HuggingFace (MIT license)
- **Code:** [manhcuong02/MeloTTS_Vietnamese](https://github.com/manhcuong02/MeloTTS_Vietnamese) on GitHub
- **Architecture:** VITS/VITS2 + PhoBERT (not vanilla BERT) + underthesea segmenter
- **Training data:** Infore ~25h (suboptimal quality — room for improvement)
- **Caveat:** Uses PhoBERT instead of official MeloTTS BERT — may need architecture adaptation for Qualcomm AI Hub Workbench export
- **Options:** (a) use via ONNX directly, (b) fine-tune further with better data, (c) adapt for Hub export

### Translation Layer — Hy-MT1.5 Discovered

Tencent's Hy-MT1.5-1.8B-1.25bit (released April 29, 2026) is a strong alternative to NLLB-600M:
- **Size:** 440MB (1.25bit quantization via Sherry framework, ACL 2026)
- **Coverage:** 33 languages, 1,056 translation directions — all 3 contest pairs in one model
- **Quality:** Surpasses Tower-Plus-72B and Qwen3-32B on Flores-200
- **On-device:** Tested on Snapdragon 888, 8x speedup over FP16, real Android APK
- **License:** Tencent HY Community License (commercial OK)
- **Tradeoff:** CPU-only (custom STQ kernel). No NPU path available.
- **Status:** Go. Hy-MT1.5 is the sole production MT model (ADR-001). NLLB excluded from production.

### NLLB-600M — Benchmark Reference Only
- License is **CC-BY-NC-4.0** (non-commercial) — not suitable for production/prize path
- **ADR-001 decision:** NLLB kept for BLEU/chrF baseline comparisons only. Not deployed on-device.
- Development workstation use only for benchmarking — no distribution or contest demo usage.

### Qualcomm AI Hub Update (v0.55.0, June 2026)
- Voice AI runtime added v0.51.0 — supports Whisper, MeloTTS, OpusMT
- MeloTTS-EN/ES/ZH available (HTP summation bug fixed v0.49.1)
- Whisper-Medium reinstated v0.51.0
- PiperTTS added v0.55.0 (en/de/it only — not VI)
- OpusMT-Zh-En on Hub (limited to single pair)
- BYOM (bring your own model) via ONNX is supported

## Current docs structure

```
docs/
  architecture.md      — System design, components, strategy, benchmarks
  contest-info.md      — Official contest rules, FAQ, timeline
  registration-checklist.md  — This file
```

---

*Generated from: Luma registration form analysis + architecture doc review. Last updated 2026-06-13.*
