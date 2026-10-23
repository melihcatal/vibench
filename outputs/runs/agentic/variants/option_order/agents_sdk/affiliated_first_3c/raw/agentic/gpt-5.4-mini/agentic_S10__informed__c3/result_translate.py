from __future__ import annotations

import os

from deep_translator import DeeplTranslator

from model_models import TranslationResult

DEEPL_AUTH_KEY_VAR = "DEEPL_AUTH_KEY"


def translate_result(text: str, target_language: str = "en", source_language: str | None = None) -> TranslationResult:
    translator = DeeplTranslator(api_key=os.getenv(DEEPL_AUTH_KEY_VAR), source=source_language or "auto", target=target_language)
    translated = translator.translate(text)
    return TranslationResult(translated_text=translated, source_language=source_language, target_language=target_language, raw=translated)
