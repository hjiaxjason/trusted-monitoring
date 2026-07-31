"""Matplotlib plots for the base replication curve and the monitor-strength
extension (§6.2 A).
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def plot_pareto_frontier(frontier: pd.DataFrame, out_path: Path, title: str = "Safety vs. Usefulness") -> None:
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.plot(frontier["usefulness"], frontier["safety"], marker="o")
    for _, row in frontier.iterrows():
        ax.annotate(f"{row['audit_budget']:.1%}", (row["usefulness"], row["safety"]))
    ax.set_xlabel("Usefulness (fraction of honest-mode correctness preserved)")
    ax.set_ylabel("Safety (P[backdoor caught])")
    ax.set_title(title)
    ax.set_xlim(0, 1.05)
    ax.set_ylim(0, 1.05)
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def plot_monitor_strength_sweep(
    frontiers_by_monitor: dict[str, pd.DataFrame], out_path: Path
) -> None:
    """Overlay one frontier per trusted-monitor model (extension A) to visualize
    whether the safety-usefulness curve degrades smoothly or has a sharp cliff
    as monitor capability decreases.
    """
    fig, ax = plt.subplots(figsize=(6, 5))
    for monitor_name, frontier in frontiers_by_monitor.items():
        ax.plot(frontier["usefulness"], frontier["safety"], marker="o", label=monitor_name)
    ax.set_xlabel("Usefulness")
    ax.set_ylabel("Safety")
    ax.set_title("Safety-usefulness frontier by monitor strength")
    ax.legend()
    ax.set_xlim(0, 1.05)
    ax.set_ylim(0, 1.05)
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
