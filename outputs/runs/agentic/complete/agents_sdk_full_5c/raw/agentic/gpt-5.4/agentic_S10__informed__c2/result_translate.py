from __future__ import annotations

import os

import deepl

from model_models import TranslationResult


def translate_result(text: str, *, target_lang: str = "EN-US") -> TranslationResult:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(text, target_lang=target_lang)
    return TranslationResult(
        translated_text=result.text,
        detected_source_language=getattr(result, "detected_source_lang", None),
        raw=result,
    )
