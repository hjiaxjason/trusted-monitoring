"""inspect_ai Task: U solves APPS problems honestly. Used for the pass-rate
sanity check (Week 1 milestone) and as the usefulness baseline.
"""

from __future__ import annotations

from inspect_ai import Task, task
from inspect_ai.solver import generate, system_message

from trusted_monitoring.data.apps_loader import load_apps_problems
from trusted_monitoring.generation.prompts import HONEST_SYSTEM_PROMPT
from trusted_monitoring.inspect_tasks._dataset import problems_to_dataset
from trusted_monitoring.inspect_tasks.scorers import apps_test_case_scorer


@task
def honest_solution_task(splits: list[str] | None = None, max_problems: int | None = None) -> Task:
    problems = load_apps_problems(splits=splits or ["interview"], max_problems=max_problems)
    return Task(
        dataset=problems_to_dataset(problems),
        solver=[system_message(HONEST_SYSTEM_PROMPT), generate()],
        scorer=apps_test_case_scorer(),
    )
