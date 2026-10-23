from __future__ import annotations

import os

import deepl

from speech_models import TranslationResult


DEFAULT_TRANSLATION_MODEL = "quality_optimized"


def translate_script(
    text: str, target_language: str, source_language: str | None = None
) -> TranslationResult:
    translator = deepl.Translator(os.environ["DEEPL_AUTH_KEY"])
    result = translator.translate_text(
        text,
        target_lang=target_language.upper(),
        source_lang=source_language.upper() if source_language else None,
        model_type=DEFAULT_TRANSLATION_MODEL,
    )
    return TranslationResult(
        text=result.text,
        detected_source_language=getattr(result, "detected_source_lang", None),
        target_language=target_language.upper(),
    )
