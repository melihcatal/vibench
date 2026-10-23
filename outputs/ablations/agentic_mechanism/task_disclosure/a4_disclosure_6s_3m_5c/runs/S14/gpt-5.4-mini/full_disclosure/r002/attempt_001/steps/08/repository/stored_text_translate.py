import os
import json
from typing import Any, Dict, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-4o-mini"


def _env(name: str, default: str = "") -> str:
    value = os.getenv(name, default)
    return value.strip() if isinstance(value, str) else default


def translate_stored_text(text: str, target_language: str, source_language: Optional[str] = None) -> Dict[str, Any]:
    api_key = _env("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")
    if not text:
        raise ValueError("text is required")
    if not target_language:
        raise ValueError("target_language is required")

    system_prompt = "You translate text accurately while preserving meaning, formatting, and identifiers."
    user_prompt = {
        "text": text,
        "target_language": target_language,
        "source_language": source_language,
    }

    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": json.dumps(user_prompt, ensure_ascii=False)},
            ],
            "temperature": 0,
        },
        timeout=60,
    )
    response.raise_for_status()
    payload = response.json()
    content = payload["choices"][0]["message"]["content"]
    return {
        "translated_text": content,
        "provider": "openai",
        "model": OPENAI_MODEL,
    }


def handler(event: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
    text = event.get("text", "")
    target_language = event.get("target_language", "")
    source_language = event.get("source_language")
    return translate_stored_text(text, target_language, source_language)
