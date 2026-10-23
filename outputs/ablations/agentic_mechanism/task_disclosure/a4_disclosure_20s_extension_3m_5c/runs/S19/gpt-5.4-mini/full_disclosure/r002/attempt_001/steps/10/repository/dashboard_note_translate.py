import os
from typing import Any, Dict, Optional

import requests


OPENAI_API_BASE = "https://api.openai.com/v1"
OPENAI_MODEL = "gpt-5.4-mini"


def translate_dashboard_note(note: str, target_locale: str, source_locale: Optional[str] = None) -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    system = (
        "You translate metric and dashboard notes accurately. "
        "Preserve identifiers, URLs, code, metric names, and formatting. "
        "Return only the translated note text."
    )
    user_parts = [f"Translate this note to {target_locale}."]
    if source_locale:
        user_parts.append(f"Source locale: {source_locale}.")
    user_parts.append(f"Note: {note}")

    payload: Dict[str, Any] = {
        "model": OPENAI_MODEL,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": " ".join(user_parts)},
        ],
        "temperature": 0.2,
    }

    response = requests.post(
        f"{OPENAI_API_BASE}/chat/completions",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()
