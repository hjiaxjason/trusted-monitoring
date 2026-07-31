import pytest

from trusted_monitoring.data.apps_loader import Problem


@pytest.fixture
def sum_two_numbers_problem() -> Problem:
    """A trivial problem used to unit-test the verifier without touching APPS."""
    return Problem(
        problem_id="test-sum",
        difficulty="interview",
        question="Read two integers from stdin, print their sum.",
        starter_code="",
        inputs=["1 2\n", "10 -5\n"],
        outputs=["3\n", "5\n"],
    )
