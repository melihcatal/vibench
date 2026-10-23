import os
from typing import Any, Dict, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-5.4-mini"


def translate_compliance_note(note: str, target_language: str, api_key: Optional[str] = None) -> str:
    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is required")

    payload: Dict[str, Any] = {
        "model": OPENAI_MODEL,
        "messages": [
            {
                "role": "system",
                "content": "Translate compliance and encryption notes accurately for reviewers without adding commentary.",
            },
            {
                "role": "user",
                "content": f"Translate the following note to {target_language}: {note}",
            },
        ],
        "temperature": 0,
    }

    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()
