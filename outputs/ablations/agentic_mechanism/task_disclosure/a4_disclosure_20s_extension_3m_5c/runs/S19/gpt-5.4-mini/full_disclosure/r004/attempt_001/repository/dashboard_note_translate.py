import os
from typing import Any, Dict, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-4o-mini"


def _build_prompt(note: str, target_locale: str) -> str:
    return (
        f"Translate the following metric or dashboard note into {target_locale}. "
        "Preserve technical meaning, metric names, identifiers, numbers, and formatting. "
        "Return only the translated text.\n\n"
        f"Note:\n{note}"
    )


def translate_dashboard_note(note: str, target_locale: str, api_key: Optional[str] = None) -> str:
    key = api_key or os.getenv("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is required")

    payload: Dict[str, Any] = {
        "model": OPENAI_MODEL,
        "messages": [
            {"role": "system", "content": "You translate observability notes accurately and concisely."},
            {"role": "user", "content": _build_prompt(note, target_locale)},
        ],
        "temperature": 0.2,
    }
    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()
