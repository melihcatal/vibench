from __future__ import annotations

import json
import os
from typing import Any, Dict, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-5.4-mini"


def translate_invoice_note(note: str, target_language: str = "en", source_language: Optional[str] = None) -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    messages = [
        {
            "role": "system",
            "content": "Translate invoice notes or descriptions accurately and concisely. Return only the translated text.",
        },
        {
            "role": "user",
            "content": json.dumps(
                {
                    "note": note,
                    "target_language": target_language,
                    "source_language": source_language,
                },
                ensure_ascii=False,
            ),
        },
    ]

    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_MODEL,
            "messages": messages,
            "temperature": 0,
        },
        timeout=30,
    )
    response.raise_for_status()
    data: Dict[str, Any] = response.json()
    return data["choices"][0]["message"]["content"].strip()
