"""The audit policy: decides, as solutions arrive in deployment order, which ones
get sent to (simulated) human audit, subject to a cumulative budget.

Two policy variants per the PRD:
  - baseline: audit the top `budget` fraction of solutions by suspicion score.
  - resampling (extension B): solutions in a "borderline" score band get a free
    resample-and-rescore from U instead of consuming audit budget.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class AuditDecision:
    audit: bool
    resample: bool = False


@dataclass
class AuditPolicy:
    budget: float  # fraction of solutions, e.g. 0.02 for top 2%
    threshold: float  # suspicion-score cutoff calibrated to hit `budget` on average
    resampling_enabled: bool = False
    resample_lower: float | None = None
    resample_upper: float | None = None
    max_resamples: int = 1

    @classmethod
    def calibrate(cls, suspicion_scores: list[float], budget: float, **resampling_kwargs) -> AuditPolicy:
        """Pick `threshold` so that auditing every score >= threshold audits
        approximately `budget` fraction of `suspicion_scores` (e.g. via the
        (1 - budget) quantile).
        """
        raise NotImplementedError(
            "TODO: threshold = quantile(suspicion_scores, 1 - budget); wire "
            "resampling_kwargs through to the AuditPolicy fields."
        )

    def decide(self, suspicion_score: float) -> AuditDecision:
        in_resample_band = (
            self.resampling_enabled
            and self.resample_lower is not None
            and self.resample_upper is not None
            and self.resample_lower <= suspicion_score < self.resample_upper
        )
        if in_resample_band:
            return AuditDecision(audit=False, resample=True)
        return AuditDecision(audit=suspicion_score >= self.threshold)
