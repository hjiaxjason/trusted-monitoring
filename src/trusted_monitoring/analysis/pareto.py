"""Aggregate per-budget DeploymentResult objects into a safety-usefulness frontier."""

from __future__ import annotations

import pandas as pd

from trusted_monitoring.audit.simulate import DeploymentResult


def compute_pareto_frontier(results: list[DeploymentResult]) -> pd.DataFrame:
    """Return a DataFrame with one row per audit budget, sorted by budget, with
    columns [audit_budget, safety, usefulness]. Downstream plotting expects this shape.
    """
    return pd.DataFrame(
        {
            "audit_budget": [r.audit_budget for r in results],
            "safety": [r.safety for r in results],
            "usefulness": [r.usefulness for r in results],
        }
    ).sort_values("audit_budget").reset_index(drop=True)
