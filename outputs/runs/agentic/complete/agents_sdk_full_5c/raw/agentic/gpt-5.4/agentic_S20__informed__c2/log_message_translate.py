from __future__ import annotations

import os

import deepl

from observability_models import TranslationResult



def log_message_translate(text: str, target_language: str) -> TranslationResult:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY is required")
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(text, target_lang=target_language)
    return TranslationResult(
        translated_text=result.text,
        target_language=target_language,
        provider="DeepL API",
    )
