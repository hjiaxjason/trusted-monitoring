#!/usr/bin/env python
"""Week 2 milestone: T scores all solutions (honest + attack, mixed and
unlabeled) for suspicion. Also loops over configs/models.yaml `trusted_sweep`
for extension A (monitor strength).

Usage: python scripts/04_run_monitor.py --honest-log results/honest.json \
    --backdoor-log results/verified_backdoors.json
"""

from __future__ import annotations

import argparse
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--honest-log", type=Path, default=Path("results/honest.json"))
    parser.add_argument("--backdoor-log", type=Path, default=Path("results/verified_backdoors.json"))
    parser.add_argument("--models-config", type=Path, default=Path("configs/models.yaml"))
    parser.add_argument("--sweep", action="store_true", help="score with every model in trusted_sweep, not just `trusted`")
    parser.add_argument("--out-dir", type=Path, default=Path("results/monitor_scores"))
    args = parser.parse_args()  # noqa: F841 (used once the TODO below is implemented)

    raise NotImplementedError(
        "TODO: load honest+backdoor logs, build a mixed & shuffled list of "
        "{problem_id, question, solution_code, is_attack, is_verified_backdoor} "
        "dicts, pass to build_monitor_dataset, then run monitor_scoring_task "
        "once per trusted model (just `trusted`, or every entry in "
        "`trusted_sweep` if --sweep), writing one results file per monitor "
        "under args.out_dir."
    )


if __name__ == "__main__":
    main()
