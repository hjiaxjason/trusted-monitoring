"""Unit tests for AuditPolicy calibration and decision logic."""

import pytest

from trusted_monitoring.audit.policy import AuditPolicy


@pytest.mark.xfail(raises=NotImplementedError, strict=True, reason="calibrate not yet implemented")
def test_calibrate_hits_target_budget_on_average():
    scores = list(range(100))  # 0..99, uniform
    policy = AuditPolicy.calibrate(scores, budget=0.1)
    n_audited = sum(1 for s in scores if policy.decide(s).audit)
    assert n_audited == pytest.approx(10, abs=1)


def test_decide_audits_above_threshold():
    policy = AuditPolicy(budget=0.1, threshold=7.0)
    assert policy.decide(8.0).audit
    assert not policy.decide(6.0).audit


def test_resampling_band_takes_priority_over_audit():
    policy = AuditPolicy(
        budget=0.1,
        threshold=7.0,
        resampling_enabled=True,
        resample_lower=4.0,
        resample_upper=7.0,
    )
    decision = policy.decide(5.0)
    assert decision.resample
    assert not decision.audit
