import os
from typing import Any, Dict, List

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-4o-mini"


def _build_messages(secret_label: str, secret_note: str) -> List[Dict[str, str]]:
    return [
        {
            "role": "system",
            "content": "You check secret labels and notes for unsafe text. Return JSON only with keys unsafe, reasons, and cleaned_text.",
        },
        {
            "role": "user",
            "content": f"Label: {secret_label}\nNote: {secret_note}",
        },
    ]


def check_secret_text(secret_label: str, secret_note: str) -> Dict[str, Any]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_MODEL,
            "messages": _build_messages(secret_label, secret_note),
            "temperature": 0,
            "response_format": {"type": "json_object"},
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def secret_label_is_safe(secret_label: str, secret_note: str) -> bool:
    result = check_secret_text(secret_label, secret_note)
    choices = result.get("choices", [])
    if not choices:
        return False
    content = choices[0].get("message", {}).get("content", "{}")
    data = __import__("json").loads(content)
    return not bool(data.get("unsafe", False))
