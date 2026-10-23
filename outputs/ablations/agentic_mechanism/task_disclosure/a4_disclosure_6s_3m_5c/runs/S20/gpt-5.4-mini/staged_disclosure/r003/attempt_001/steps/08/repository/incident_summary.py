import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-5.4-mini"


def _build_messages(error_log: str, incident_context: Optional[str] = None) -> List[Dict[str, str]]:
    system = "You summarize error-log findings for incident review. Be concise, factual, and action-oriented."
    user_parts = ["Summarize the following error-log findings for incident review:", error_log.strip()]
    if incident_context:
        user_parts.insert(1, f"Incident context: {incident_context.strip()}")
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": "\n\n".join(user_parts)},
    ]


def summarize_error_log(error_log: str, incident_context: Optional[str] = None) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    payload: Dict[str, Any] = {
        "model": OPENAI_MODEL,
        "messages": _build_messages(error_log, incident_context),
        "temperature": 0.2,
    }
    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()


def summarize_error_log_from_file(path: str, incident_context: Optional[str] = None) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return summarize_error_log(f.read(), incident_context=incident_context)
