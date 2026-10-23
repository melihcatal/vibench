#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
PYTHON_BIN="${PYTHON_BIN:-python}"

if [[ $# -lt 1 || "$1" == "--help" ]]; then
  printf '%s\n' 'Usage: bash ablations/shared/scripts/run_sequential.sh OUTPUT_ROOT [--models MODEL_LIST] [runner flags] [--execute]' \
    'Models run in parallel within each ablation. Ablations run strictly 1, then 2, then 3, then 4.' \
    'Default: validate only. No new no-anchor or agentic-baseline runs.' \
    'Each stage uses its own default scope; ablation 4 reads agentic_mechanism/task_disclosure/config.yaml. Explicit scope flags override defaults.'
  exit 0
fi
OUTPUT="$1"
shift
COMMON=()
EXECUTE=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    --execute) EXECUTE=1; shift ;;
    --models) COMMON+=("$1" "${2:?--models requires a value}"); shift 2 ;;
    --s11-legacy-ack) printf '%s\n' 'Legacy S11 override removed: the reviewed migrated anchor is required.' >&2; exit 2 ;;
    --output|--output=*|--conditions|--conditions=*|--check|--limit|--limit=*|--config|--config=*)
      printf 'Unsupported suite flag: %s. Use an individual runner for limited/partial runs.\n' "$1" >&2; exit 2 ;;
    *) COMMON+=("$1"); shift ;;
  esac
done
cd "$ROOT"

# Stage numbers stay 1-4 because they appear in archived run manifests and in
# the analysis snapshots; this maps each to its campaign directory.
stage_path() {
  case "$1" in
    1) printf '%s' 'ablations/initial_provider/assigned_as_code' ;;
    2) printf '%s' 'ablations/agentic_mechanism/single_shot_multifile' ;;
    3) printf '%s' 'ablations/initial_provider/by_instruction' ;;
    4) printf '%s' 'ablations/agentic_mechanism/task_disclosure' ;;
    *) printf 'Unknown ablation stage: %s\n' "$1" >&2; exit 2 ;;
  esac
}

run_stage() {
  local stage="$1" mode="$2"
  local command=("$PYTHON_BIN" -u -B "$(stage_path "$stage")/scripts/run.py"
    ${COMMON[@]+"${COMMON[@]}"} --output "$OUTPUT/ablation_${stage}" "$mode")
  "${command[@]}"
}

# Validate all four scopes before any paid call; no background stage processes.
for stage in 1 2 3 4; do
  run_stage "$stage" --check
done
if [[ "$EXECUTE" -eq 0 ]]; then
  printf '%s\n' 'All stages validated. No model calls made.'
  exit 0
fi
for stage in 1 2 3 4; do
  printf '\nStarting ablation %s; waiting for every model before the next stage.\n' "$stage"
  run_stage "$stage" --execute
done
