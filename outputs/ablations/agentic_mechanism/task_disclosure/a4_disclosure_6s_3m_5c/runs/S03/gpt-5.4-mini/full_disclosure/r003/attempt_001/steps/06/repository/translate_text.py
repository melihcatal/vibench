import os
from typing import Any, Dict, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = os.getenv("OPENAI_TRANSLATION_MODEL", "gpt-4.1-mini")


def translate_text(text: str, source_language: str, target_language: str, temperature: float = 0.0, timeout: int = 60) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload: Dict[str, Any] = {
        "model": OPENAI_MODEL,
        "temperature": temperature,
        "messages": [
            {
                "role": "system",
                "content": f"You are a translation engine. Translate from {source_language} to {target_language}. Return only the translated text.",
            },
            {"role": "user", "content": text},
        ],
    }

    response = requests.post(OPENAI_API_URL, headers=headers, json=payload, timeout=timeout)
    response.raise_for_status()
    data: Dict[str, Any] = response.json()
    choices = data.get("choices") or []
    if not choices:
        raise ValueError("No translation returned by OpenAI")
    message = choices[0].get("message") or {}
    content = message.get("content")
    if not isinstance(content, str):
        raise ValueError("Invalid translation response")
    return content.strip()
