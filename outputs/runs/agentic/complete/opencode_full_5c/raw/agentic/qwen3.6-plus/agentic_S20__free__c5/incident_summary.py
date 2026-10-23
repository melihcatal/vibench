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


def summarize_error_findings(
    error_entries: list[LogEntry],
    max_tokens: int = 1024,
) -> str:
    log_summaries = []
    for entry in error_entries:
        log_summaries.append(
            f"[{entry.timestamp}] [{entry.status}] service={entry.service} "
            f"host={entry.hostname} message={entry.message} "
            f"attrs={json.dumps(entry.attributes)}"
        )

    log_context = "\n".join(log_summaries)

    system_prompt = (
        "You are an incident response analyst. Review the provided error log entries "
        "and produce a structured incident summary. Include: root cause hypothesis, "
        "affected services, severity assessment, timeline of events, and recommended "
        "next steps. Be concise and actionable."
    )

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {get_openai_api_key()}",
    }

    payload = {
        "model": OPENAI_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": f"Error log entries to analyze:\n\n{log_context}",
            },
        ],
        "max_tokens": max_tokens,
        "temperature": 0.3,
    }

    resp = requests.post(OPENAI_API_URL, headers=headers, json=payload, timeout=60)
    resp.raise_for_status()
    result = resp.json()
    return result["choices"][0]["message"]["content"]


if __name__ == "__main__":
    sample_entries = [
        LogEntry(
            id="log-001",
            message="Connection pool exhausted",
            status="error",
            service="db-proxy",
            hostname="prod-db-01",
            timestamp="2025-01-15T10:23:01Z",
            attributes={"pool_size": 50, "active_connections": 50},
        ),
        LogEntry(
            id="log-002",
            message="Request timeout after 30s",
            status="error",
            service="api-gateway",
            hostname="prod-gw-03",
            timestamp="2025-01-15T10:23:15Z",
            attributes={"endpoint": "/api/orders", "timeout_ms": 30000},
        ),
    ]
    summary = summarize_error_findings(sample_entries)
    print(summary)
