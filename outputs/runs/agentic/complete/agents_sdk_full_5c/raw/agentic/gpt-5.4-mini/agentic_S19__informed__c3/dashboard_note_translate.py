from __future__ import annotations

import os

import deepl

from observability_models import TranslationResult


def dashboard_note_translate(text: str, target_language: str, source_language: str | None = None) -> TranslationResult:
    translator = deepl.Translator(os.getenv("DEEPL_AUTH_KEY", ""))
    result = translator.translate_text(text, target_lang=target_language, source_lang=source_language)
    return TranslationResult(source_text=text, translated_text=str(result), target_language=target_language, source_language=source_language, provider="deepl")
