import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = "gpt-5.4-mini"
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"


def _build_messages(messages: List[str], target_locale: str) -> List[Dict[str, str]]:
    joined = "\n".join(f"- {message}" for message in messages)
    return [
        {
            "role": "system",
            "content": "Translate support-visible log messages accurately, preserving placeholders, identifiers, timestamps, codes, and technical tokens.",
        },
        {
            "role": "user",
            "content": f"Translate the following log messages into {target_locale}. Return a JSON array of translated strings in the same order.\n\n{joined}",
        },
    ]


def translate_log_messages(messages: List[str], target_locale: str) -> List[str]:
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY is required")
    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_MODEL,
            "messages": _build_messages(messages, target_locale),
            "temperature": 0,
        },
        timeout=60,
    )
    response.raise_for_status()
    data: Dict[str, Any] = response.json()
    content = data["choices"][0]["message"]["content"]
    parsed = __import__("json").loads(content)
    if not isinstance(parsed, list):
        raise ValueError("Expected a JSON array of translated messages")
    return [str(item) for item in parsed]
