from __future__ import annotations

import os

from deepl import Translator

from identity_models import TranslationResult


DEEPL_MODEL_TYPE = os.getenv("DEEPL_MODEL_TYPE", "prefer_quality_optimized")


def translate_consent_copy(text: str, target_language: str, source_language: str = "EN") -> TranslationResult:
    translator = Translator(os.environ["DEEPL_AUTH_KEY"])
    result = translator.translate_text(
        text,
        source_lang=source_language,
        target_lang=target_language,
        model_type=DEEPL_MODEL_TYPE,
    )
    return TranslationResult(
        provider="deepl",
        model=DEEPL_MODEL_TYPE,
        source_language=source_language,
        target_language=target_language,
        translated_text=result.text,
    )
