#!/usr/bin/env python
"""Week 3 milestone: sweep audit budgets (configs/audit.yaml), bootstrap
deployment order, and compute safety/usefulness per budget per monitor.

Usage: python scripts/05_simulate_audit.py --monitor-scores-dir results/monitor_scores
"""

from __future__ import annotations

import argparse
from pathlib import Path

import yaml


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--monitor-scores-dir", type=Path, default=Path("results/monitor_scores"))
    parser.add_argument("--audit-config", type=Path, default=Path("configs/audit.yaml"))
    parser.add_argument("--out", type=Path, default=Path("results/deployment_results.json"))
    args = parser.parse_args()

    audit_config = yaml.safe_load(args.audit_config.read_text())  # noqa: F841 (used below)

    raise NotImplementedError(
        "TODO: for each monitor's score file in args.monitor_scores_dir, build "
        "SolutionRecord list, then for each budget in "
        "audit_config['audit_budgets']: AuditPolicy.calibrate(...), "
        "simulate_deployment(records, policy, bootstrap_runs="
        "audit_config['bootstrap_runs']); collect DeploymentResults keyed by "
        "monitor name, serialize to args.out."
    )


if __name__ == "__main__":
    main()
