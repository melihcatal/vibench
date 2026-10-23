#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON_BIN="${PYTHON_BIN:-python}"
if [[ $# -lt 1 || "$1" == --help ]]; then
  printf '%s\n' 'Usage: bash ablations/run_all.sh OUTPUT_ROOT [--execute] [--resume] [--retry-failed] [runner options]' \
    'Default: dry validation; A1-A3 use 20 scenarios/6 models, A4 uses its YAML (6 scenarios/3 models), all 5 repetitions.' \
    'Models run in parallel; ablations run sequentially. Keys load from code/configs/.env.' \
    'Use --models, --scenarios, --repetitions or --workers to override the scope.' \
    'A full default campaign has 3,180 repository/response runs, including 180 ten-request ablation-4 runs.'
  exit 0
fi
OUTPUT="$1"
shift
exec bash "$ROOT/ablations/shared/scripts/run_sequential.sh" "$OUTPUT" \
  "$@"
