import os
from typing import Any, Dict, List

import requests


ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"
ANTHROPIC_MODEL = "claude-3-5-sonnet-20240620"


def translate_compliance_note(note: str, target_language: str = "en") -> str:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY is required")

    payload: Dict[str, Any] = {
        "model": ANTHROPIC_MODEL,
        "max_tokens": 1024,
        "messages": [
            {
                "role": "user",
                "content": (
                    f"Translate the following encryption or compliance note into {target_language}. "
                    "Preserve technical meaning, policy references, and security terminology.\n\n"
                    f"Note:\n{note}"
                ),
            }
        ],
    }
    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }
    response = requests.post(ANTHROPIC_API_URL, json=payload, headers=headers, timeout=60)
    response.raise_for_status()
    data = response.json()
    content: List[Dict[str, Any]] = data.get("content", [])
    parts = [item.get("text", "") for item in content if item.get("type") == "text"]
    return "".join(parts).strip()
