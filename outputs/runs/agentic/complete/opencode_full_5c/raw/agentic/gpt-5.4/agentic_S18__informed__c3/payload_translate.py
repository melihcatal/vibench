from __future__ import annotations

import os

import deepl

from messaging_models import TranslationResult


def translate_payload_text(text: str, target_language: str) -> TranslationResult:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("Missing required environment variable: DEEPL_AUTH_KEY")
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(text, target_lang=target_language)
    return TranslationResult(
        translated_text=result.text,
        detected_source_language=getattr(result, "detected_source_lang", None),
        target_language=target_language,
        provider="DeepL API",
    )
