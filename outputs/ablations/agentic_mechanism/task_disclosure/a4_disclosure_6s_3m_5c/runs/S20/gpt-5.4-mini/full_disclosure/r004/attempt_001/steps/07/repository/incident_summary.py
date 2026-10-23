import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-5.4-mini"


def _headers() -> Dict[str, str]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    return {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}


def _build_prompt(error_logs: List[Dict[str, Any]], incident_context: Optional[str]) -> str:
    context = incident_context.strip() if incident_context else ""
    return (
        "Summarize the following error-log findings for incident review. "
        "Focus on likely root cause, blast radius, timeline, notable patterns, and recommended next steps. "
        "Keep it concise and actionable.\n\n"
        f"Incident context: {context or 'N/A'}\n\n"
        f"Error logs: {error_logs}"
    )


def summarize_incident(error_logs: List[Dict[str, Any]], incident_context: Optional[str] = None) -> str:
    payload = {
        "model": OPENAI_MODEL,
        "messages": [
            {"role": "system", "content": "You summarize operational incidents from logs."},
            {"role": "user", "content": _build_prompt(error_logs, incident_context)},
        ],
        "temperature": 0.2,
    }
    response = requests.post(OPENAI_API_URL, headers=_headers(), json=payload, timeout=60)
    response.raise_for_status()
    data = response.json()
    choices = data.get("choices", [])
    if not choices:
        raise RuntimeError("No summary returned by OpenAI")
    message = choices[0].get("message", {})
    content = message.get("content")
    if not content:
        raise RuntimeError("Empty summary returned by OpenAI")
    return content
