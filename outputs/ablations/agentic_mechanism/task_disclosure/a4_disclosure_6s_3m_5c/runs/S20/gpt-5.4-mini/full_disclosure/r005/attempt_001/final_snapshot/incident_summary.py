import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_API_BASE = "https://api.openai.com/v1"
OPENAI_MODEL = "gpt-5.4-mini"


def _build_prompt(logs: List[Dict[str, Any]], incident_context: Optional[str] = None) -> str:
    context = incident_context.strip() if incident_context else ""
    lines = [
        "Summarize these error-log findings for an incident review.",
        "Focus on likely impact, affected components, common failure patterns, timestamps, and next investigative steps.",
    ]
    if context:
        lines.append(f"Incident context: {context}")
    lines.append("Error logs:")
    for idx, log in enumerate(logs, 1):
        lines.append(f"{idx}. {log}")
    return "\n".join(lines)


def summarize_error_logs(logs: List[Dict[str, Any]], incident_context: Optional[str] = None) -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    prompt = _build_prompt(logs, incident_context)
    response = requests.post(
        f"{OPENAI_API_BASE}/responses",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_MODEL,
            "input": prompt,
        },
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    output = data.get("output", [])
    texts: List[str] = []
    for item in output:
        for content in item.get("content", []):
            text = content.get("text")
            if text:
                texts.append(text)
    if texts:
        return "\n".join(texts).strip()
    return data.get("output_text", "").strip()
