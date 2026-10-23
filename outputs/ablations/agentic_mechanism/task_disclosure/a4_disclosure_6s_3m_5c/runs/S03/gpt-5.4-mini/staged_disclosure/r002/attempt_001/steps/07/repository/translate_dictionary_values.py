import os
from typing import Any, Dict

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"


def _translate_text(text: str, target_language: str, source_language: str = "auto") -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    prompt = f"Translate the following text from {source_language} to {target_language}. Return only the translation. Text: {text}"
    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": "You are a translation engine."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0,
        },
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()


def translate_dictionary_values(data: Dict[str, Any], target_language: str, source_language: str = "auto") -> Dict[str, Any]:
    translated: Dict[str, Any] = {}
    for key, value in data.items():
        if isinstance(value, str):
            translated[key] = _translate_text(value, target_language, source_language)
        else:
            translated[key] = value
    return translated
