import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.4-mini")


def _auth_headers() -> Dict[str, str]:
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY is required")
    return {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }


def summarize_incident(error_logs: List[Dict[str, Any]], incident_context: str = "") -> str:
    if not error_logs:
        return "No error-log findings were provided for incident review."

    prompt = {
        "model": OPENAI_MODEL,
        "messages": [
            {
                "role": "system",
                "content": "You summarize error-log findings for incident review. Be concise, factual, and include likely impact, key patterns, and next investigative steps.",
            },
            {
                "role": "user",
                "content": {
                    "incident_context": incident_context,
                    "error_logs": error_logs,
                },
            },
        ],
        "temperature": 0.2,
    }

    response = requests.post(
        f"{OPENAI_API_BASE.rstrip('/')}/chat/completions",
        headers=_auth_headers(),
        json=prompt,
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()


def summarize_error_log_findings(error_logs: List[Dict[str, Any]], incident_context: str = "") -> str:
    return summarize_incident(error_logs, incident_context)
