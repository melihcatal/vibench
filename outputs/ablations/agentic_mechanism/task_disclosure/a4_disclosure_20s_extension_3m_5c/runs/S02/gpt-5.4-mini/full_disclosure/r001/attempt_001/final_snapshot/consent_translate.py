import os
from typing import Optional

import requests


OPENAI_TRANSLATE_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-5.4-mini"


def translate_consent_copy(text: str, target_language: str, source_language: Optional[str] = None) -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    messages = [
        {
            "role": "system",
            "content": "Translate identity-provider consent copy accurately, preserving meaning, tone, and any placeholders.",
        },
        {
            "role": "user",
            "content": {
                "text": text,
                "target_language": target_language,
                "source_language": source_language,
            },
        },
    ]

    response = requests.post(
        OPENAI_TRANSLATE_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
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
    payload = response.json()
    return payload["choices"][0]["message"]["content"].strip()
