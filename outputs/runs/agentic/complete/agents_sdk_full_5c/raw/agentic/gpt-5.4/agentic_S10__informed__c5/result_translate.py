from __future__ import annotations

import os

import deepl

from model_models import TranslationResult


DEFAULT_TARGET_LANG = "DE"


def translate_result(text: str, target_language: str = DEFAULT_TARGET_LANG) -> TranslationResult:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise RuntimeError("DEEPL_AUTH_KEY is required")
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(text, target_lang=target_language)
    return TranslationResult(
        translated_text=result.text,
        target_language=target_language,
        provider="DeepL API",
    )
