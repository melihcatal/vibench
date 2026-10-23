from __future__ import annotations

import os

import deepl

from model_models import TranslationResult


def translate_result(text: str, target_language: str, source_language: str | None = None) -> TranslationResult:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY is required")

    translator = deepl.Translator(auth_key)
    result = translator.translate_text(
        text,
        target_lang=target_language,
        source_lang=source_language,
        preserve_formatting=True,
    )
    return TranslationResult(
        provider="deepl",
        translated_text=result.text,
        target_language=target_language,
        detected_source_language=getattr(result, "detected_source_lang", source_language),
        raw=result,
    )
