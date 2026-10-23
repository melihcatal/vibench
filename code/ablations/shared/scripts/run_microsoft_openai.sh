#!/usr/bin/env bash
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
PYTHON_BIN="${PYTHON_BIN:-python}"
MODE="--check"
RETRY=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --execute) MODE="--execute" ;;
    --retry-failed) RETRY=(--retry-failed) ;;
    --help|-h)
      printf '%s\n' \
        'Usage: bash ablations/shared/scripts/run_microsoft_openai.sh [--execute] [--retry-failed]' \
        'Runs only the A1 and A3 Microsoft/OpenAI additions, sequentially.' \
        'Default: offline validation. --execute authorizes generation.' \
        'Resumes existing campaigns; failures are retried only with --retry-failed.' \
        'Continues after ordinary stage failures, but stops on interruption.'
      exit 0 ;;
    *) printf 'Unknown argument: %s\n' "$1" >&2; exit 2 ;;
  esac
  shift
done

trap 'printf "\nInterrupted; no further ablation will start.\n" >&2; exit 130' INT
trap 'printf "\nTerminated; no further ablation will start.\n" >&2; exit 143' TERM
cd "$ROOT" || exit 1

# Stage numbers stay 1 and 3 because they appear in archived run manifests;
# this maps each to its campaign directory.
stage_path() {
  case "$1" in
    1) printf '%s' 'ablations/initial_provider/assigned_as_code' ;;
    3) printf '%s' 'ablations/initial_provider/by_instruction' ;;
    *) printf 'Unknown stage: %s\n' "$1" >&2; exit 2 ;;
  esac
}

STATUS=0
for stage in 1 3; do
  printf '\nStarting A%s Microsoft/OpenAI extension (%s).\n' "$stage" "$MODE"
  campaign="$(stage_path "$stage")"
  "$PYTHON_BIN" -u -B "$campaign/microsoft_openai/scripts/run.py" \
    --config "$campaign/microsoft_openai/config.yaml" \
    --output "../outputs/$campaign/microsoft_openai/a${stage}_microsoft_openai_20s_3m_5c" \
    --resume ${RETRY[@]+"${RETRY[@]}"} "$MODE"
  code=$?
  printf '\nA%s finished with exit code %s.\n' "$stage" "$code"
  case "$code" in
    130|143) exit "$code" ;;
    0) ;;
    *) STATUS=1; printf 'A%s reported failures; saved outputs are retained.\n' "$stage" >&2 ;;
  esac
done

if [[ "$STATUS" -ne 0 ]]; then
  printf '\nBoth stages attempted. Inspect failed runs before using the results.\n' >&2
else
  printf '\nBoth stages finished successfully (%s).\n' "$MODE"
fi
exit "$STATUS"
