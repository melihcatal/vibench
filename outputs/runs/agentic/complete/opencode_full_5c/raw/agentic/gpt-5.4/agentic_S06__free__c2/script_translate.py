from __future__ import annotations

import os

import requests

from speech_models import TranslationResult, ensure_text


GOOGLE_TRANSLATE_URL = "https://translation.googleapis.com/language/translate/v2"


def translate_script(
    text: str, target_language: str, source_language: str | None = None
) -> TranslationResult:
    api_key = os.environ.get("GOOGLE_TRANSLATE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_TRANSLATE_API_KEY is required")
    payload = {
        "q": ensure_text(text),
        "target": target_language,
        "format": "text",
        "key": api_key,
    }
    if source_language:
        payload["source"] = source_language
    response = requests.post(GOOGLE_TRANSLATE_URL, data=payload, timeout=30)
    response.raise_for_status()
    translated = response.json()["data"]["translations"][0]
    return TranslationResult(
        translated_text=translated["translatedText"],
        source_language=translated.get("detectedSourceLanguage", source_language),
        target_language=target_language,
    )
