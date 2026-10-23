import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = os.getenv("OPENAI_TRANSLATE_MODEL", "gpt-4o-mini")


def translate_onboarding_copy(text: str, locale: str, source_language: Optional[str] = None) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    system_prompt = "Translate onboarding copy accurately, preserving meaning, tone, and formatting."
    user_prompt = {
        "locale": locale,
        "source_language": source_language,
        "text": text,
    }

    payload: Dict[str, Any] = {
        "model": OPENAI_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": str(user_prompt)},
        ],
        "temperature": 0.2,
    }

    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    choices: List[Dict[str, Any]] = data.get("choices", [])
    if not choices:
        raise RuntimeError("OpenAI translation response did not contain choices")

    message = choices[0].get("message", {})
    content = message.get("content")
    if not isinstance(content, str) or not content.strip():
        raise RuntimeError("OpenAI translation response did not contain text")
    return content.strip()
