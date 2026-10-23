from __future__ import annotations

import os

import deepl

from storage_models import TranslationResult


def translate_extracted_text(
    text: str, target_language: str, source_language: str | None = None
) -> TranslationResult:
    auth_key = os.environ["DEEPL_AUTH_KEY"]
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(
        text, target_lang=target_language, source_lang=source_language
    )
    detected_source = source_language or getattr(result, "detected_source_lang", None)
    return TranslationResult(
        provider="deepl",
        source_language=detected_source,
        target_language=target_language,
        translated_text=result.text,
    )
