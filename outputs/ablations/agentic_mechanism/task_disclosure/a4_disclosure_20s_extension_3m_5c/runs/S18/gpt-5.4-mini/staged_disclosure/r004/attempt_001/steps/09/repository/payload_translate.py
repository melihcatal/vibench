import os
from typing import Any, Dict, List, Union

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-5.4-mini"


def _translate_text(text: str, target_language: str, api_key: str) -> str:
    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_MODEL,
            "messages": [
                {"role": "system", "content": "Translate customer-facing text accurately and preserve meaning, tone, placeholders, and formatting."},
                {"role": "user", "content": f"Translate the following text to {target_language}: {text}"},
            ],
            "temperature": 0,
        },
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()


def _translate_value(value: Any, target_language: str, api_key: str) -> Any:
    if isinstance(value, str):
        return _translate_text(value, target_language, api_key)
    if isinstance(value, list):
        return [_translate_value(item, target_language, api_key) for item in value]
    if isinstance(value, dict):
        return {key: _translate_value(item, target_language, api_key) for key, item in value.items()}
    return value


def translate_payload(payload: Dict[str, Any], target_language: str, api_key: str = None) -> Dict[str, Any]:
    key = api_key or os.getenv("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is required")
    return _translate_value(payload, target_language, key)
