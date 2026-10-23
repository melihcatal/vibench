from __future__ import annotations

import os

import deepl

from identity_models import TranslationResult


DEEPL_MODEL_TYPE = "prefer_quality_optimized"


def translate_consent_copy(text: str, target_language: str, source_language: str | None = None) -> TranslationResult:
    translator = deepl.Translator(os.environ["DEEPL_AUTH_KEY"])
    result = translator.translate_text(
        text,
        source_lang=source_language,
        target_lang=target_language,
        model_type=DEEPL_MODEL_TYPE,
    )
    return TranslationResult(
        translated_text=result.text,
        detected_source_language=getattr(result, "detected_source_lang", source_language),
        target_language=target_language,
        provider="DeepL",
        raw={
            "billed_characters": getattr(result, "billed_characters", None),
            "detected_source_lang": getattr(result, "detected_source_lang", None),
            "model_type": DEEPL_MODEL_TYPE,
        },
    )
