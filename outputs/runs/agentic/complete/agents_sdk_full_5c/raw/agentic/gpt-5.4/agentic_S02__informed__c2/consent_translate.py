from __future__ import annotations

import os

import deepl

from identity_models import TranslationResult


DEEPL_MODEL = "DeepL API"


def translate_consent_copy(text: str, target_language: str, source_language: str | None = None) -> TranslationResult:
    translator = deepl.Translator(os.environ["DEEPL_AUTH_KEY"])
    result = translator.translate_text(
        text,
        target_lang=target_language.upper(),
        source_lang=source_language.upper() if source_language else None,
    )
    return TranslationResult(
        translated_text=result.text,
        source_language=getattr(result, "detected_source_lang", source_language),
        target_language=target_language.upper(),
        provider=DEEPL_MODEL,
        raw={
            "billed_characters": getattr(result, "billed_characters", None),
            "detected_source_lang": getattr(result, "detected_source_lang", None),
        },
    )
