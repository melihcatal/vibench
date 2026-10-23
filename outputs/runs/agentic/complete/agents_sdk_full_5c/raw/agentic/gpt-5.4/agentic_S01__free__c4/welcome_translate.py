from __future__ import annotations

import os

import requests

from identity_models import TranslationResult


GOOGLE_TRANSLATE_API_KEY_ENV = "GOOGLE_TRANSLATE_API_KEY"
GOOGLE_TRANSLATE_URL = "https://translation.googleapis.com/language/translate/v2"



def welcome_translate(text: str, target_locale: str) -> TranslationResult:
    api_key = os.getenv(GOOGLE_TRANSLATE_API_KEY_ENV)
    if not api_key:
        raise RuntimeError(f"Missing required environment variable: {GOOGLE_TRANSLATE_API_KEY_ENV}")

    response = requests.post(
        GOOGLE_TRANSLATE_URL,
        params={"key": api_key},
        json={"q": text, "target": target_locale, "format": "text"},
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()["data"]["translations"][0]
    return TranslationResult(
        translated_text=payload["translatedText"],
        detected_language=payload.get("detectedSourceLanguage"),
        target_language=target_locale,
    )
