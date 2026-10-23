from __future__ import annotations

import os

import deepl

from speech_models import TranslationResult


DEEPL_MODEL_TYPE = "quality_optimized"


def translate_script(text: str, target_language: str, source_language: str | None = None) -> TranslationResult:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise EnvironmentError("DEEPL_AUTH_KEY is required for DeepL API.")
    translator = deepl.Translator(auth_key)
    response = translator.translate_text(
        text,
        source_lang=source_language,
        target_lang=target_language,
        model_type=DEEPL_MODEL_TYPE,
    )
    return TranslationResult(
        translated_text=response.text,
        detected_source_language=getattr(response, "detected_source_lang", source_language),
        provider="deepl",
    )
