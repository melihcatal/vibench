from __future__ import annotations

import os

import requests

from identity_models import TranslationResult


DEEPL_API_URL = "https://api-free.deepl.com/v2/translate"


def translate_consent_copy(text: str, target_language: str) -> TranslationResult:
    response = requests.post(
        DEEPL_API_URL,
        data={"text": text, "target_lang": target_language.upper()},
        headers={"Authorization": f"DeepL-Auth-Key {os.environ['DEEPL_API_KEY']}"},
        timeout=20,
    )
    response.raise_for_status()
    payload = response.json()
    translation = payload["translations"][0]
    return TranslationResult(
        provider="deepl",
        target_language=target_language.upper(),
        translated_text=translation["text"],
        detected_source_language=translation.get("detected_source_language"),
    )
