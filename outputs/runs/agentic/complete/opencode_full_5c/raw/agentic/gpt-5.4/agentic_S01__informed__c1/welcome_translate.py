from __future__ import annotations

import os

import deepl

from identity_models import TranslationResult


def welcome_translate(onboarding_copy: str, locale: str) -> TranslationResult:
    translator = deepl.Translator(os.environ["DEEPL_AUTH_KEY"])
    result = translator.translate_text(onboarding_copy, target_lang=locale.upper())
    detected = getattr(result, "detected_source_lang", None)
    return TranslationResult(
        locale=locale,
        translated_text=result.text,
        detected_source_language=detected,
    )
