from __future__ import annotations

import requests

from storage_client import google_translate_api_key
from storage_models import TranslationResult


GOOGLE_TRANSLATE_ENDPOINT = "https://translation.googleapis.com/language/translate/v2"


def translate_stored_text(
    text: str, target_language: str, source_language: str | None = None
) -> TranslationResult:
    payload: dict[str, str] = {
        "q": text,
        "target": target_language,
        "format": "text",
        "key": google_translate_api_key(),
    }
    if source_language:
        payload["source"] = source_language
    response = requests.post(GOOGLE_TRANSLATE_ENDPOINT, data=payload, timeout=60)
    response.raise_for_status()
    data = response.json()["data"]["translations"][0]
    return TranslationResult(
        source_text=text,
        translated_text=data["translatedText"],
        source_language=data.get("detectedSourceLanguage") or source_language,
        target_language=target_language,
        provider="google-translate",
    )
