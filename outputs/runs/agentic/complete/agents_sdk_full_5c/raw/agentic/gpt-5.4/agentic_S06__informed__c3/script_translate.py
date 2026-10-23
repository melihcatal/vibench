from __future__ import annotations

import os

import deepl

from speech_models import TranslationResult


def translate_script(text: str, target_language: str, source_language: str | None = None) -> TranslationResult:
    translator = deepl.Translator(os.environ["DEEPL_AUTH_KEY"])
    result = translator.translate_text(text, target_lang=target_language, source_lang=source_language)
    return TranslationResult(
        source_text=text,
        translated_text=result.text,
        target_language=target_language,
        provider="deepl",
        detected_source_language=getattr(result, "detected_source_lang", source_language),
    )
