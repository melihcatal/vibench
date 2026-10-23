from __future__ import annotations

import os

import deepl

from model_models import TranslationResult


def localize_platform_output(text: str, target_language: str) -> TranslationResult:
    client = deepl.Translator(os.environ["DEEPL_AUTH_KEY"])
    result = client.translate_text(text, target_lang=target_language)
    return TranslationResult(
        text=result.text,
        target_language=target_language,
        detected_source_language=getattr(result, "detected_source_lang", None),
        raw={
            "billed_characters": getattr(result, "billed_characters", None),
            "detected_source_lang": getattr(result, "detected_source_lang", None),
            "provider": "deepl",
        },
    )
