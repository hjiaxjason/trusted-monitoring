#!/usr/bin/env python
"""Aggregate attack-mode eval logs into a clean verified-backdoors dataset,
tracking failed attacks (didn't pass visible tests, or backdoor didn't trigger)
separately rather than silently dropping them, per PRD §6.1 step 2.

Usage: python scripts/03_verify_backdoors.py --attack-log results/attack.json
"""

from __future__ import annotations

import argparse
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--attack-log", type=Path, default=Path("results/attack.json"))
    parser.add_argument("--out", type=Path, default=Path("results/verified_backdoors.json"))
    args = parser.parse_args()  # noqa: F841 (used once the TODO below is implemented)

    raise NotImplementedError(
        "TODO: read the inspect_ai eval log at args.attack_log, pull "
        "VerificationResult metadata written by backdoor_verification_scorer, "
        "split into verified_backdoors vs failed_attacks, report attack success "
        "rate = len(verified_backdoors) / len(all attack attempts), write both "
        "lists to args.out."
    )


if __name__ == "__main__":
    main()
