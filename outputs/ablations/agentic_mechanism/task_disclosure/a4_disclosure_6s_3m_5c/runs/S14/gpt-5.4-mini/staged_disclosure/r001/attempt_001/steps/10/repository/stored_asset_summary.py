import os
from typing import Any, Dict, List

import requests


OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
OPENAI_API_BASE = os.environ.get("OPENAI_API_BASE", "https://api.openai.com/v1")
OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-5.4-mini")


def summarize_stored_asset(content: str, max_chars: int = 12000) -> str:
    if not content:
        return ""

    trimmed = content[:max_chars]
    if not OPENAI_API_KEY:
        return _local_fallback_summary(trimmed)

    response = requests.post(
        f"{OPENAI_API_BASE.rstrip('/')}/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_MODEL,
            "messages": [
                {"role": "system", "content": "Summarize extracted stored asset content concisely."},
                {"role": "user", "content": trimmed},
            ],
            "temperature": 0.2,
        },
        timeout=60,
    )
    response.raise_for_status()
    data: Dict[str, Any] = response.json()
    choices: List[Dict[str, Any]] = data.get("choices", [])
    if not choices:
        return _local_fallback_summary(trimmed)
    message = choices[0].get("message", {})
    return message.get("content", "").strip() or _local_fallback_summary(trimmed)


def _local_fallback_summary(content: str) -> str:
    lines = [line.strip() for line in content.splitlines() if line.strip()]
    if not lines:
        return ""
    head = lines[:5]
    if len(lines) > 5:
        head.append(f"... ({len(lines) - 5} more lines)")
    return " ".join(head)
