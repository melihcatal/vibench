import os
from typing import Any, Dict

import requests


OPENAI_CHAT_COMPLETIONS_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-4o-mini"


def translate_payload(payload: Dict[str, Any], target_language: str = "en") -> Dict[str, Any]:
    text = str(payload.get("text", ""))
    if not text:
        return payload

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("OPENAI_API_KEY is required")

    response = requests.post(
        OPENAI_CHAT_COMPLETIONS_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": "Translate customer-facing message payload text while preserving meaning, tone, placeholders, and formatting.",
                },
                {
                    "role": "user",
                    "content": f"Translate this text to {target_language}: {text}",
                },
            ],
            "temperature": 0,
        },
        timeout=30,
    )
    response.raise_for_status()
    translated_text = response.json()["choices"][0]["message"]["content"].strip()

    result = dict(payload)
    result["text"] = translated_text
    return result
