#!/usr/bin/env bash
# Run the full pipeline end to end. With --smoke, restricts to a tiny problem
# subset so this finishes in minutes on CPU (used by the CI smoke test).
set -euo pipefail

cd "$(dirname "$0")/.."

MAX_PROBLEMS_FLAG=()
if [[ "${1:-}" == "--smoke" ]]; then
  MAX_PROBLEMS_FLAG=(--max-problems 5)
fi

python scripts/01_generate_honest.py "${MAX_PROBLEMS_FLAG[@]}"
python scripts/02_generate_attack.py "${MAX_PROBLEMS_FLAG[@]}"
python scripts/03_verify_backdoors.py
python scripts/04_run_monitor.py
python scripts/05_simulate_audit.py
python scripts/06_plot_pareto.py

echo "Done. See results/pareto_base.png"
