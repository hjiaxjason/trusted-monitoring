#!/usr/bin/env python
"""Week 1 milestone: U generates honest solutions; sanity-check pass rate.

Usage: python scripts/01_generate_honest.py [--max-problems N] [--out results/honest.json]
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from inspect_ai import eval as inspect_eval

from trusted_monitoring.inspect_tasks.honest_task import honest_solution_task


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--splits", nargs="+", default=["interview"])
    parser.add_argument("--max-problems", type=int, default=None)
    parser.add_argument("--out", type=Path, default=Path("results/honest.json"))
    args = parser.parse_args()

    logs = inspect_eval(
        honest_solution_task(splits=args.splits, max_problems=args.max_problems),
        model="hf/local",  # TODO: resolve from configs/models.yaml `untrusted` entry
    )

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps({"n_logs": len(logs)}, indent=2))
    print(f"Wrote honest-mode results summary to {args.out}")


if __name__ == "__main__":
    main()
