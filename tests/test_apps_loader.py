"""Unit tests for the APPS loading/filtering utilities."""

import pytest

from trusted_monitoring.data.apps_loader import _parse_io, load_apps_problems


def test_parse_io_valid():
    raw = '{"inputs": ["1 2\\n"], "outputs": ["3\\n"]}'
    inputs, outputs = _parse_io(raw)
    assert inputs == ["1 2\n"]
    assert outputs == ["3\n"]


def test_parse_io_malformed_returns_empty():
    assert _parse_io("not json") == ([], [])
    assert _parse_io(None) == ([], [])


@pytest.mark.xfail(raises=NotImplementedError, strict=True, reason="load_apps_problems not yet implemented")
def test_load_apps_problems_filters_by_min_test_cases():
    problems = load_apps_problems(splits=["interview"], max_problems=10, min_test_cases=2)
    assert all(len(p.inputs) >= 2 for p in problems)
