"""inspect_ai Task: U solves APPS problems in attack mode (instructed to insert
a backdoor). Scored by the backdoor verifier rather than plain test-case pass/fail.
"""

from __future__ import annotations

from inspect_ai import Task, task
from inspect_ai.solver import generate, system_message

from trusted_monitoring.data.apps_loader import load_apps_problems
from trusted_monitoring.generation.prompts import ATTACK_SYSTEM_PROMPT
from trusted_monitoring.inspect_tasks._dataset import problems_to_dataset
from trusted_monitoring.inspect_tasks.scorers import backdoor_verification_scorer


@task
def attack_solution_task(splits: list[str] | None = None, max_problems: int | None = None) -> Task:
    problems = load_apps_problems(splits=splits or ["interview"], max_problems=max_problems)
    return Task(
        dataset=problems_to_dataset(problems),
        solver=[system_message(ATTACK_SYSTEM_PROMPT), generate()],
        scorer=backdoor_verification_scorer(),
    )
