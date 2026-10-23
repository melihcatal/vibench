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


def translate_log_messages(
    log_entries: list[LogEntry],
    target_language: str = "es",
) -> list[dict[str, Any]]:
    results = []
    for entry in log_entries:
        translated = _translate_single_entry(entry, target_language)
        results.append(translated)
    return results


def _translate_single_entry(entry: LogEntry, target_language: str) -> dict[str, Any]:
    system_prompt = (
        f"You are a technical translator specializing in software log messages. "
        f"Translate the provided log message into {target_language}. Preserve all "
        f"technical terms, variable names, identifiers, and structured data exactly "
        f"as they appear. Only translate natural-language portions. Return a JSON "
        f"object with keys: 'original' (the original message), 'translated' (the "
        f"translated message), and 'language' (the target language code)."
    )

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {get_openai_api_key()}",
    }

    payload = {
        "model": OPENAI_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": entry.message},
        ],
        "max_tokens": 256,
        "temperature": 0.0,
        "response_format": {"type": "json_object"},
    }

    resp = requests.post(OPENAI_API_URL, headers=headers, json=payload, timeout=60)
    resp.raise_for_status()
    result = resp.json()
    translation = json.loads(result["choices"][0]["message"]["content"])

    return {
        "log_id": entry.id,
        "original": translation.get("original", entry.message),
        "translated": translation.get("translated", entry.message),
        "language": translation.get("language", target_language),
        "status": entry.status,
        "service": entry.service,
        "timestamp": entry.timestamp,
    }


if __name__ == "__main__":
    sample_entries = [
        LogEntry(
            id="log-t01",
            message="Database connection failed: unable to reach primary host",
            status="error",
            service="db-proxy",
            hostname="prod-db-01",
            timestamp="2025-01-15T10:23:01Z",
        ),
        LogEntry(
            id="log-t02",
            message="Rate limit exceeded for client IP 10.0.0.55",
            status="warning",
            service="api-gateway",
            hostname="prod-gw-02",
            timestamp="2025-01-15T10:24:30Z",
        ),
    ]
    translations = translate_log_messages(sample_entries, target_language="es")
    print(json.dumps(translations, indent=2))
