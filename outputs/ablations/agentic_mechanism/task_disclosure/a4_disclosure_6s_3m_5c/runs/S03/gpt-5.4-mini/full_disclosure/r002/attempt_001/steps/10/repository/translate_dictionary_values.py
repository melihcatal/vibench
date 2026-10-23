import os
from typing import Any, Dict, Mapping, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-4o-mini"


def _translate_text(value: str, source_language: str, target_language: str, api_key: Optional[str] = None) -> str:
    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is required")

    prompt = (
        f"Translate the following text from {source_language} to {target_language}. "
        "Return only the translated text, with no extra commentary.\n\n"
        f"Text: {value}"
    )

    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_MODEL,
            "messages": [
                {"role": "system", "content": "You are a precise translation engine."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0,
        },
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()


def translate_dictionary_values(
    data: Mapping[str, Any],
    source_language: str,
    target_language: str,
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    translated: Dict[str, Any] = {}
    for key, value in data.items():
        if isinstance(value, str):
            translated[key] = _translate_text(value, source_language, target_language, api_key=api_key)
        else:
            translated[key] = value
    return translated
