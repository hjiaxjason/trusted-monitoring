"""Load and filter the APPS dataset (codeparrot/apps) for the trusted-monitoring pipeline."""

from __future__ import annotations

import json
from dataclasses import dataclass, field


@dataclass
class Problem:
    problem_id: str
    difficulty: str
    question: str
    starter_code: str
    inputs: list[str]
    outputs: list[str]
    metadata: dict = field(default_factory=dict)


def load_apps_problems(
    splits: list[str],
    max_problems: int | None = None,
    seed: int = 0,
    min_test_cases: int = 2,
) -> list[Problem]:
    """Load APPS problems for the given difficulty splits, filtered to those with
    at least `min_test_cases` parseable input/output pairs (the "reliable test
    cases" filter called for in the PRD).

    Raises NotImplementedError until wired up to `datasets.load_dataset`.
    """
    raise NotImplementedError(
        "TODO: datasets.load_dataset('codeparrot/apps', split=...), parse the "
        "'input_output' JSON field, drop problems with unparseable or empty "
        "test cases, subsample to max_problems with the given seed."
    )


def _parse_io(input_output_raw: str) -> tuple[list[str], list[str]]:
    """Parse the raw `input_output` JSON string APPS stores per-problem into
    (inputs, outputs) lists. Returns ([], []) if the field is missing/malformed.
    """
    try:
        parsed = json.loads(input_output_raw)
    except (json.JSONDecodeError, TypeError):
        return [], []
    return parsed.get("inputs", []), parsed.get("outputs", [])
