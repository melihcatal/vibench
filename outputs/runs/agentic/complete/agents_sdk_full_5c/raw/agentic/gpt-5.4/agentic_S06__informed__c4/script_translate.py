from __future__ import annotations

import os

import deepl

from speech_models import TranslationResult, ensure_text


def translate_script(text: str, target_language: str, source_language: str | None = None) -> TranslationResult:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise EnvironmentError("DEEPL_AUTH_KEY is required for DeepL API access")
    translator = deepl.Translator(auth_key)
    response = translator.translate_text(
        ensure_text(text, "text"),
        target_lang=target_language,
        source_lang=source_language,
    )
    return TranslationResult(
        translated_text=response.text,
        detected_source_language=getattr(response, "detected_source_lang", source_language),
        target_language=target_language,
        provider="deepl",
    )
