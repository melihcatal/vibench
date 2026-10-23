import os
import json
from typing import Any

import requests

from observability_models import LogEntry


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-4o"


def get_openai_api_key() -> str:
    key = os.environ.get("OPENAI_API_KEY", "")
    if not key:
        raise RuntimeError("OPENAI_API_KEY environment variable is required")
    return key


def check_log_text_safety(
    log_entries: list[LogEntry],
) -> list[dict[str, Any]]:
    results = []
    for entry in log_entries:
        safety_result = _evaluate_single_entry(entry)
        results.append(safety_result)
    return results


def _evaluate_single_entry(entry: LogEntry) -> dict[str, Any]:
    text_to_check = f"message: {entry.message}"
    if entry.attributes:
        attr_text = json.dumps(entry.attributes)
        text_to_check += f"\nattributes: {attr_text}"

    system_prompt = (
        "You are a content safety reviewer for log messages. Analyze the provided log "
        "text and determine if it contains any unsafe content such as: personally "
        "identifiable information (PII), secrets or credentials, payment card data, "
        "sensitive internal identifiers, or content that violates data handling policies. "
        "Return a JSON object with keys: 'safe' (boolean), 'risk_level' (one of: none, "
        "low, medium, high, critical), 'findings' (list of specific concerns or empty), "
        "and 'redacted_text' (the text with any unsafe values replaced by [REDACTED])."
    )

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {get_openai_api_key()}",
    }

    payload = {
        "model": OPENAI_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text_to_check},
        ],
        "max_tokens": 512,
        "temperature": 0.0,
        "response_format": {"type": "json_object"},
    }

    resp = requests.post(OPENAI_API_URL, headers=headers, json=payload, timeout=60)
    resp.raise_for_status()
    result = resp.json()
    analysis = json.loads(result["choices"][0]["message"]["content"])

    return {
        "log_id": entry.id,
        "safe": analysis.get("safe", True),
        "risk_level": analysis.get("risk_level", "none"),
        "findings": analysis.get("findings", []),
        "redacted_text": analysis.get("redacted_text", ""),
    }


if __name__ == "__main__":
    sample_entries = [
        LogEntry(
            id="log-s01",
            message="User authenticated with email john@example.com and SSN 123-45-6789",
            status="info",
            service="auth-service",
            hostname="prod-auth-01",
            timestamp="2025-01-15T11:00:00Z",
            attributes={"api_key": "sk-live-abc123secret"},
        ),
        LogEntry(
            id="log-s02",
            message="Health check passed",
            status="info",
            service="api-gateway",
            hostname="prod-gw-01",
            timestamp="2025-01-15T11:00:05Z",
            attributes={},
        ),
    ]
    safety_results = check_log_text_safety(sample_entries)
    print(json.dumps(safety_results, indent=2))
