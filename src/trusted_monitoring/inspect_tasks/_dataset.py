"""Convert our Problem objects into an inspect_ai Dataset, shared by all tasks."""

from __future__ import annotations

from inspect_ai.dataset import MemoryDataset, Sample

from trusted_monitoring.data.apps_loader import Problem


def problems_to_dataset(problems: list[Problem]) -> MemoryDataset:
    samples = [
        Sample(
            id=p.problem_id,
            input=p.question,
            metadata={
                "difficulty": p.difficulty,
                "starter_code": p.starter_code,
                "inputs": p.inputs,
                "outputs": p.outputs,
                **p.metadata,
            },
        )
        for p in problems
    ]
    return MemoryDataset(samples=samples)
