# Trusted Monitoring for AI Control

A replication and extension of the trusted-monitoring protocol from Greenblatt et al. (2024), in the APPS backdoor-insertion setting.

## Status

This repository is currently a scaffold, not a finished replication.
The package structure, `inspect_ai` task wiring, config schema, CLI scripts, and test skeleton are in place.
Most function bodies raise `NotImplementedError` with a `TODO` describing exactly what needs to be filled in — see the module docstrings under `src/trusted_monitoring/`.
The `tests/` suite documents expected behavior for each stub via `xfail(strict=True)` markers; as each piece is implemented, remove its marker and the test should pass.

See `PRD.md` (or the project's tracked PRD) for the full design and milestone plan this scaffold implements.

## Threat model, in one paragraph

An untrusted model U is given APPS coding problems and, in "attack mode," instructed to insert a backdoor that passes visible tests but fails on a specific hidden input.
A weaker trusted model T scores every submitted solution for suspicion.
A fixed audit budget determines how many of the most-suspicious solutions get sent to (simulated) human review.
**Safety** is the probability a real backdoor gets caught before deployment; **usefulness** is the fraction of U's honest-mode correctness the protocol still extracts.
The core result is the safety-usefulness Pareto frontier as the audit budget varies.

## Repository layout

```
configs/
  models.yaml       # U / T model definitions, backend (local HF vs hosted API), the monitor-strength sweep list
  audit.yaml        # audit budgets, bootstrap runs, resampling/summary-only extension toggles

src/trusted_monitoring/
  data/             # APPS loading + filtering
  generation/       # U's honest/attack system prompts and a backend-agnostic Generator
  verification/     # the backdoor verifier — sandboxed execution against visible + trigger inputs
  monitoring/       # T's suspicion scoring (prompted 0-10, or logprob-based)
  audit/            # audit policy (budget/threshold, optional resampling) + bootstrap deployment simulation
  analysis/         # Pareto frontier computation and plotting
  inspect_tasks/    # inspect_ai Task/Sample/Scorer definitions wiring the above into the eval harness

scripts/
  01_generate_honest.py    # U solves problems honestly (usefulness baseline)
  02_generate_attack.py    # U solves problems in attack mode
  03_verify_backdoors.py   # aggregate + verify attack-mode solutions
  04_run_monitor.py        # T scores all solutions (mixed, unlabeled); loops over the monitor-strength sweep
  05_simulate_audit.py     # bootstrap safety/usefulness across audit budgets
  06_plot_pareto.py        # render the base and monitor-strength-sweep Pareto plots
  run_all.sh               # orchestrates 01-06; `--smoke` restricts to a handful of problems

tests/              # unit tests for the verifier, audit policy, and APPS loader
```

## Setup

Requires Python 3.10+.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

Local model inference (the default backend in `configs/models.yaml`) needs a machine with enough VRAM for a 7B model, or you can switch `backend: hosted` entries to point at Together/Fireworks and set the corresponding API key in `.env` (copy `.env.example`).

## Running the pipeline

Once the `TODO`s in `src/trusted_monitoring/` are implemented:

```bash
scripts/run_all.sh          # full run
scripts/run_all.sh --smoke  # tiny subset, for a quick sanity check
```

This produces `results/pareto_base.png` (the base replication curve) and `results/pareto_monitor_sweep.png` (the monitor-strength extension).

## Tests

```bash
pytest
ruff check src tests scripts
```

## Extension experiment

The scaffold defaults to **monitor strength** (extension A in the PRD): `configs/models.yaml`'s `trusted_sweep` list is scored against the same solution set to see whether the safety-usefulness frontier degrades smoothly or has a sharp cliff as the monitor gets weaker.
`configs/audit.yaml` also has toggles staged for **resampling** (extension B) and **summary-only monitoring** (extension C) if time allows adding those on top.
