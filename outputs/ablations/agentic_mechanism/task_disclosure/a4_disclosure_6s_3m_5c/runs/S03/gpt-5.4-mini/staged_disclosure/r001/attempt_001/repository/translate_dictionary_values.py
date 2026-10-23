import os
from typing import Any, Dict

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-4o-mini"


def translate_text(text: str, target_language: str, source_language: str = "auto") -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": "You translate text accurately and preserve meaning.",
                },
                {
                    "role": "user",
                    "content": f"Translate the following text from {source_language} to {target_language}: {text}",
                },
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
            translated[key] = translate_text(value, target_language, source_language)
        elif isinstance(value, dict):
            translated[key] = translate_dictionary_values(value, target_language, source_language)
        elif isinstance(value, list):
            translated[key] = [
                translate_dictionary_values(item, target_language, source_language)
                if isinstance(item, dict)
                else translate_text(item, target_language, source_language)
                if isinstance(item, str)
                else item
                for item in value
            ]
        else:
            translated[key] = value
    return translated


if __name__ == "__main__":
    sample = {"hello": "world", "nested": {"goodbye": "friend"}}
    print(translate_dictionary_values(sample, "Spanish"))
