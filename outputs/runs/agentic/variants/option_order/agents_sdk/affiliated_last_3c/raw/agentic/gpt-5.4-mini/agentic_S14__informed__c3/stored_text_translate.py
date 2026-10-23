from __future__ import annotations

import os

from google.cloud import translate_v2 as translate

from storage_models import TranslationResult


PROJECT_NOTE = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "")


def stored_text_translate(text: str, target_language: str = "en", source_language: str | None = None) -> TranslationResult:
    client = translate.Client()
    translated = client.translate(text, target_language=target_language, source_language=source_language)
    return TranslationResult(
        source_text=text,
        translated_text=translated.get("translatedText", ""),
        source_lang=translated.get("detectedSourceLanguage") or source_language,
        target_lang=target_language,
        provider="google-cloud-translate",
    )
