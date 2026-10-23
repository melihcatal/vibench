from __future__ import annotations

import os

import deepl

from model_models import TranslationResult


def translate_result(
    text: str, target_language: str, source_language: str | None = None
) -> TranslationResult:
    client = deepl.Translator(os.environ["DEEPL_AUTH_KEY"])
    result = client.translate_text(
        text, target_lang=target_language, source_lang=source_language
    )
    detected = getattr(result, "detected_source_lang", None)
    return TranslationResult(
        provider="deepl",
        translated_text=result.text,
        target_language=target_language,
        detected_source_language=detected,
    )
