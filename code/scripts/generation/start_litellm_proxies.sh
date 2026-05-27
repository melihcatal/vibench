#!/usr/bin/env bash
set -euo pipefail

# Start the local LiteLLM proxy routes used by the OpenCode agentic runner.
#
# The Python runners load configs/.env themselves, but these proxy processes are
# separate shell commands. This helper sources configs/.env before launching the
# proxies so AWS/IBM credentials are available to LiteLLM.

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
ENV_FILE="${VIBENCH_ENV_FILE:-${ROOT_DIR}/configs/.env}"

if [[ ! -f "${ENV_FILE}" ]]; then
  echo "Missing ${ENV_FILE}."
  echo "Create it with: cp configs/.env.template configs/.env"
  exit 1
fi

if ! command -v litellm >/dev/null 2>&1; then
  echo "Missing litellm command. Install dependencies first:"
  echo "  pip install -r requirements.txt"
  exit 1
fi

set -a
# shellcheck disable=SC1090
source "${ENV_FILE}"
set +a

BEDROCK_PORT="${LITELLM_BEDROCK_PORT:-4000}"
WATSONX_PORT="${LITELLM_WATSONX_PORT:-4001}"

BEDROCK_MODEL="${LITELLM_BEDROCK_MODEL:-bedrock/eu.amazon.nova-pro-v1:0}"
BEDROCK_ALIAS="${LITELLM_BEDROCK_ALIAS:-nova-pro}"

WATSONX_MODEL="${LITELLM_WATSONX_MODEL:-watsonx/ibm/granite-4-h-small}"
WATSONX_ALIAS="${LITELLM_WATSONX_ALIAS:-granite-4.0-h-small}"

echo "Starting LiteLLM Bedrock proxy: ${BEDROCK_ALIAS} -> ${BEDROCK_MODEL} on port ${BEDROCK_PORT}"
litellm --model "${BEDROCK_MODEL}" --alias "${BEDROCK_ALIAS}" --port "${BEDROCK_PORT}" --drop_params &
bedrock_pid=$!

echo "Starting LiteLLM watsonx proxy: ${WATSONX_ALIAS} -> ${WATSONX_MODEL} on port ${WATSONX_PORT}"
litellm --model "${WATSONX_MODEL}" --alias "${WATSONX_ALIAS}" --port "${WATSONX_PORT}" --drop_params &
watsonx_pid=$!

cleanup() {
  kill "${bedrock_pid}" "${watsonx_pid}" 2>/dev/null || true
}
trap cleanup EXIT INT TERM

echo
echo "Proxies are running. Keep this terminal open while run_agentic.py runs."
echo "Expected OpenCode base URLs:"
echo "  LITELLM_BEDROCK_API_BASE=${LITELLM_BEDROCK_API_BASE:-http://127.0.0.1:${BEDROCK_PORT}/v1}"
echo "  LITELLM_WATSONX_API_BASE=${LITELLM_WATSONX_API_BASE:-http://127.0.0.1:${WATSONX_PORT}/v1}"

wait
