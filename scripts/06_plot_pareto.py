#!/usr/bin/env python
"""Week 3-4 milestone: render the base replication Pareto curve and the
monitor-strength sweep overlay (extension A).

Usage: python scripts/06_plot_pareto.py --deployment-results results/deployment_results.json
"""

from __future__ import annotations

import argparse
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--deployment-results", type=Path, default=Path("results/deployment_results.json"))
    parser.add_argument("--out-dir", type=Path, default=Path("results"))
    args = parser.parse_args()  # noqa: F841 (used once the TODO below is implemented)

    raise NotImplementedError(
        "TODO: load args.deployment_results (monitor_name -> list of "
        "DeploymentResult-shaped dicts), reconstruct DeploymentResult objects, "
        "call compute_pareto_frontier per monitor, plot_pareto_frontier for the "
        "primary `trusted` monitor to out_dir/pareto_base.png, and "
        "plot_monitor_strength_sweep across all monitors to "
        "out_dir/pareto_monitor_sweep.png."
    )


if __name__ == "__main__":
    main()
