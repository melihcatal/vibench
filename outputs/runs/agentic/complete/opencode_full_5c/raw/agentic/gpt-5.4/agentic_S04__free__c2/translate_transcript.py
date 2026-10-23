from __future__ import annotations

import os

import requests


DEEPL_API_URL = "https://api-free.deepl.com/v2/translate"
DEEPL_API_KEY_ENV = "DEEPL_API_KEY"


def translate_transcript(
    segments: list[dict[str, object]], target_language: str
) -> list[dict[str, object]]:
    api_key = os.getenv(DEEPL_API_KEY_ENV)
    if not api_key:
        raise RuntimeError(
            f"Missing required environment variable: {DEEPL_API_KEY_ENV}"
        )
    texts = [str(segment.get("text", "")) for segment in segments]
    response = requests.post(
        DEEPL_API_URL,
        data={"target_lang": target_language.upper(), "text": texts},
        headers={"Authorization": f"DeepL-Auth-Key {api_key}"},
        timeout=60,
    )
    response.raise_for_status()
    translations = response.json().get("translations", [])
    return [
        {
            **segment,
            "translated_text": translations[index].get("text", "")
            if index < len(translations)
            else "",
            "provider": "deepl",
        }
        for index, segment in enumerate(segments)
    ]
