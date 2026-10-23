from __future__ import annotations

import os

import requests

from vision_models import TranslationResult


DEEPL_API_URL = "https://api.deepl.com/v2/translate"


def alt_text_translate(description: str, target_language: str) -> TranslationResult:
    response = requests.post(
        DEEPL_API_URL,
        headers={"Authorization": f"DeepL-Auth-Key {os.environ['DEEPL_API_KEY']}"},
        data={"text": description, "target_lang": target_language},
        timeout=60,
    )
    response.raise_for_status()
    payload = response.json()
    translated_text = payload["translations"][0]["text"]
    return TranslationResult(
        provider="deepl",
        translated_text=translated_text,
        target_language=target_language,
    )
