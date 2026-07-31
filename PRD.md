# PRD: Trusted Monitoring for AI Control — Replication & Extension

## 1. Summary

Reimplement the core trusted-monitoring protocol from Greenblatt et al. (2024) in the APPS backdoor-insertion setting, produce a safety–usefulness Pareto frontier, then extend the protocol along one or two axes (monitor strength, resampling, or action-summary-only monitoring) to generate a novel result.
Ship as a public, documented GitHub repo with reproducible experiments.

## 2. Motivation

- AI control asks: even if we can't verify a model is aligned, can we design deployment protocols where a misaligned model can't cause catastrophic harm?
  Trusted monitoring is the foundational protocol in this agenda.
- The original result hasn't been broadly re-derived by outside researchers; a clean, well-documented replication is genuine signal for control-focused fellowships (SPAR, MATS) even before any extension.
- Extending it (rather than pure replication) turns this from a class-project artifact into something closer to a small research contribution.

## 3. Goals

1. Reproduce the basic trusted-monitoring safety–usefulness tradeoff curve on APPS.
2. Build reusable infrastructure (red-team model, blue-team monitor, scoring harness) that supports swapping in new protocols cheaply.
3. Run at least one extension experiment beyond the base replication and report the result, positive or negative.
4. Publish a repo with a README that a stranger could use to reproduce every plot in under an hour of compute.

## 4. Non-goals

- Not attempting agentic/multi-step environments (file system, shell tools) — that's a natural v2, not this PRD.
- Not trying to beat published numbers or claim a new SOTA protocol.
- Not building a general-purpose control-evals framework — reuse `inspect-ai` or similar rather than reinventing harness infrastructure.

## 5. Background / setup

**Threat model:** an untrusted model (U) is given coding problems (APPS dataset) and instructed to solve them while secretly inserting a backdoor (code that passes visible tests but fails on a specific hidden input).
A weaker trusted model (T) monitors U's output and flags suspicious solutions for human/audit review, subject to a fixed audit budget.

**Core tradeoff:** safety (probability an inserted backdoor is caught before causing harm) vs. usefulness (how much of U's raw capability the protocol still extracts, since overly aggressive flagging throws away good solutions).

**Models (open-weight, no frontier API needed):**
- U (untrusted, "smart"): Qwen2.5-Coder-7B-Instruct or DeepSeek-Coder-6.7B — capable enough to write good code and follow subtle backdoor instructions.
- T (trusted, "weak"): Qwen2.5-Coder-1.5B-Instruct or similar — deliberately weaker, stands in for a trusted-but-limited monitor.
- Optional third role: a stronger trusted model used only for the "trusted editing" baseline if time allows.

**Dataset:** APPS (codeparrot/apps on HF), interview + competition difficulty splits, filtered to problems with reliable test cases.

## 6. Technical design

### 6.1 Pipeline stages

1. **Solution generation (U):** prompt U to solve each problem two ways — (a) honest baseline, (b) "attack" mode with a system prompt instructing it to insert a backdoor undetectable to a weaker reviewer while still passing visible tests.
2. **Backdoor verification:** for attack-mode solutions, automatically verify the backdoor is real (passes visible tests, fails on the hidden trigger input) — discard "failed attacks" from the attack set or track them separately.
3. **Monitoring (T):** T scores every submitted solution (attack and honest, mixed and unlabeled to T) for suspicion, e.g. 0–10 scale via prompted self-report, or log-prob-based scoring.
4. **Audit policy:** given a fixed audit budget (e.g. top 2% most-suspicious flagged for "human review" = ground-truth check), compute:
   - **Safety** = P(a real backdoor is caught | it was inserted), across many simulated deployment runs (bootstrap over problem order, since audit budget is cumulative).
   - **Usefulness** = fraction of U's honest-mode correctness preserved after the protocol filters/replaces flagged solutions.
5. **Sweep:** vary audit budget and monitor threshold to trace the full Pareto frontier, replicating the shape of the original paper's curve.

### 6.2 Extension experiment (pick one for v1)

- **A — Monitor strength sweep:** repeat the full pipeline with 2–3 different T models of varying capability; plot how the Pareto frontier shifts.
  Tests whether "how much weaker can the monitor be" has a sharp cliff or a smooth degradation.
- **B — Resampling:** when T flags a solution as borderline (not high enough to audit, not low enough to trust), resample from U and re-score, spending extra inference compute instead of audit budget.
  Compare resulting frontier to the no-resampling baseline.
- **C — Summary-only monitoring:** instead of showing T the full code, show it only a natural-language summary of what the code does (generated by U or a third model) and see how much safety is lost — a cheaper, more scalable monitoring mode.

Recommendation: start with **A**, since it reuses the exact same harness with no new mechanism, de-risking the replication.
Add **B** or **C** only if time remains.

### 6.3 Stack

- `inspect-ai` for eval harness scaffolding (task definition, scoring, transcript logging) — matches tooling labs actually use.
- HF `transformers` + local/Colab GPU or a cheap inference API (Together, Fireworks) for the 1.5B–7B models — keeps cost near $0 with local models, or a few dollars with hosted inference.
- `pandas` / `matplotlib` for the Pareto curve analysis (you already have this stack).
- GitHub Actions for a lightweight "reproduce smoke test" on a small problem subset, so the badge on your README isn't a lie.

## 7. Milestones (suggested ~4-week timeline)

| Week | Milestone | Deliverable |
|---|---|---|
| 1 | Setup + honest baseline | Repo scaffold, APPS loader, U generates honest solutions, pass-rate sanity check |
| 1–2 | Attack pipeline | U attack-mode prompting, automatic backdoor verifier, attack success rate measured |
| 2 | Monitor + scoring | T scores all solutions, suspicion-score distributions plotted for honest vs. attack sets |
| 3 | Audit simulation + base Pareto curve | Safety/usefulness computed across audit budgets, base replication plot matches expected shape |
| 3–4 | Extension experiment (A/B/C) | Second Pareto curve or degradation plot for the chosen extension |
| 4 | Writeup + polish | README with reproduction steps, plots, 1-page results summary (optionally a short arXiv-style writeup) |

## 8. Success metrics

- Base replication reproduces the qualitative shape of the original safety–usefulness tradeoff (safety rises steeply then plateaus as audit budget increases).
- Extension experiment produces a clear, interpretable result (even a null result, if well-characterized, counts).
- A stranger can clone the repo, run one script, and regenerate the main plot within an hour on a single GPU or via hosted inference.
- Repo is legible enough to link directly in a SPAR/MATS application.

## 9. Risks / open questions

- **Attack realism:** small open models may be bad at inserting subtle backdoors on instruction alone — may need few-shot examples of backdoor techniques from the original paper's appendix.
- **Monitor calibration:** a 1.5B model prompted for a 0–10 suspicion score may have noisy, uncalibrated outputs — worth comparing prompted scoring vs. a simple log-prob-based signal.
- **Compute budget:** full sweeps across many problems × multiple audit budgets × multiple monitor models can add up; may need to subsample APPS rather than run the full set.
- **Verification correctness:** the backdoor verifier (checking pass-visible/fail-hidden) is load-bearing for the whole safety metric — needs its own unit tests before trusting downstream numbers.

## 10. Out of scope for v1 (future work)

- Agentic/tool-use control environments.
- Untrusted monitoring or collusion between U and a second untrusted model.
- Human-in-the-loop audit (using an LLM as the "auditor" proxy is fine for v1).
