from __future__ import annotations

import os

from google.cloud import translate_v2 as translate

from identity_models import TranslationResult


GOOGLE_TRANSLATE_TARGET_ENV = "GOOGLE_TRANSLATE_DEFAULT_TARGET"


def translate_consent_copy(text: str, target_language: str | None = None) -> TranslationResult:
    client = translate.Client()
    target = target_language or os.getenv(GOOGLE_TRANSLATE_TARGET_ENV, "en")
    response = client.translate(text, target_language=target, format_="text")
    return TranslationResult(
        provider="Google Cloud Translation",
        target_language=target,
        translated_text=response["translatedText"],
        detected_source_language=response.get("detectedSourceLanguage"),
        raw=response,
    )
