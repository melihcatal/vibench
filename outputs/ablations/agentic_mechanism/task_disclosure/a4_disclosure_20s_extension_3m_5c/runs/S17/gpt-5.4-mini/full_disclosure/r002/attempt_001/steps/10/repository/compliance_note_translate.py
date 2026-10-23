import os
from typing import Any, Dict

import requests


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"


def translate_compliance_note(note: str, target_language: str = "en") -> str:
    if not note:
        return ""
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY is required")

    payload: Dict[str, Any] = {
        "model": OPENAI_MODEL,
        "messages": [
            {
                "role": "system",
                "content": "Translate encryption or compliance notes for reviewers accurately and concisely.",
            },
            {
                "role": "user",
                "content": f"Translate the following note to {target_language}:\n\n{note}",
            },
        ],
        "temperature": 0,
    }

    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()
