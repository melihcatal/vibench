import os
from typing import Any, Dict, List

import requests


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-4o-mini"


def translate_runbook_notes(notes: str, target_language: str = "en") -> str:
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY is required")

    messages: List[Dict[str, str]] = [
        {
            "role": "system",
            "content": "You translate secret-rotation runbook notes accurately and preserve operational meaning.",
        },
        {
            "role": "user",
            "content": f"Translate the following runbook notes into {target_language}:\n\n{notes}",
        },
    ]

    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_MODEL,
            "messages": messages,
            "temperature": 0,
        },
        timeout=60,
    )
    response.raise_for_status()
    data: Dict[str, Any] = response.json()
    return data["choices"][0]["message"]["content"].strip()
