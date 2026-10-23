from __future__ import annotations

import os

import deepl

from speech_models import TranslationResult


def translate_script(
    text: str, target_language: str, source_language: str | None = None
) -> TranslationResult:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise EnvironmentError("DEEPL_AUTH_KEY is required")
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(
        text, target_lang=target_language, source_lang=source_language
    )
    detected_source = getattr(result, "detected_source_lang", source_language)
    return TranslationResult(
        translated_text=result.text,
        source_language=detected_source,
        target_language=target_language,
        provider="deepl",
    )
