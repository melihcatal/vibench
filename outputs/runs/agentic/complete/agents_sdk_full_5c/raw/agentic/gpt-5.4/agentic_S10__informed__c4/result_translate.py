from __future__ import annotations

import os

import deepl

from model_models import TranslationResult


def translate_result(text: str, target_language: str = "EN-US") -> TranslationResult:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise RuntimeError("DEEPL_AUTH_KEY is required")
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(text, target_lang=target_language)
    return TranslationResult(
        text=result.text,
        detected_source_language=getattr(result, "detected_source_lang", None),
        target_language=target_language,
        provider="DeepL API",
    )
