from __future__ import annotations

import os

import deepl

from identity_models import TranslationResult


def welcome_translate(text: str, target_locale: str) -> TranslationResult:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise RuntimeError("Missing required environment variable: DEEPL_AUTH_KEY")
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(text, target_lang=target_locale.upper())
    return TranslationResult(
        source_text=text,
        translated_text=result.text,
        target_locale=target_locale,
        provider="deepl",
    )
