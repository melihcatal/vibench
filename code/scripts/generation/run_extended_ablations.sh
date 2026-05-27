#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT_DIR"

MODE="${1:-sequential}"

run_direct() {
  local name="$1"
  python scripts/generation/run_direct.py \
    --config "configs/vibench/direct/ablations/option_order/${name}_3c.yaml" \
    --resume "direct/ablations/option_order/${name}_3c" \
    --retry-errors \
    --retry-empty
}

run_opencode() {
  local name="$1"
  python scripts/generation/run_agentic.py \
    --config "configs/vibench/agentic/ablations/option_order/opencode/${name}_3c.yaml" \
    --resume "agentic/ablations/option_order/opencode/${name}_3c" \
    --retry-errors \
    --retry-empty \
    --retry-incomplete
}

run_agents_sdk() {
  local name="$1"
  python scripts/generation/run_agentic_litellm_agents.py \
    --config "configs/vibench/agentic/ablations/option_order/agents_sdk/${name}_3c.yaml" \
    --resume "agentic/ablations/option_order/agents_sdk/${name}_3c" \
    --retry-errors \
    --retry-empty \
    --retry-incomplete
}

run_direct_suite() {
  run_direct affiliated_first
  run_direct affiliated_middle
  run_direct affiliated_last
  run_direct affiliated_omitted
}

run_opencode_suite() {
  run_opencode affiliated_first
  run_opencode affiliated_middle
  run_opencode affiliated_last
  run_opencode affiliated_omitted
}

run_agents_sdk_suite() {
  run_agents_sdk affiliated_first
  run_agents_sdk affiliated_last
}

usage() {
  cat <<'EOF'
Usage:
  bash scripts/generation/run_extended_ablations.sh [sequential|parallel-families]

Modes:
  sequential
    Runs all ablation resumes one after another. Safest mode.

  parallel-families
    Runs three background chains in parallel:
      1. direct ablations sequentially
      2. OpenCode ablations sequentially
      3. Agents SDK ablations sequentially
    Faster, but more likely to hit shared provider rate limits.
EOF
}

case "$MODE" in
  sequential)
    run_direct_suite
    run_opencode_suite
    run_agents_sdk_suite
    ;;
  parallel-families)
    run_direct_suite &
    pid_direct=$!
    run_opencode_suite &
    pid_opencode=$!
    run_agents_sdk_suite &
    pid_agents=$!

    wait "$pid_direct"
    wait "$pid_opencode"
    wait "$pid_agents"
    ;;
  -h|--help|help)
    usage
    ;;
  *)
    echo "Unknown mode: $MODE" >&2
    echo >&2
    usage >&2
    exit 1
    ;;
esac
