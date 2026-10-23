from __future__ import annotations

import os

import deepl

from identity_models import TranslationResult


def welcome_translate(text: str, target_locale: str) -> dict:
    translator = deepl.Translator(os.environ["DEEPL_AUTH_KEY"])
    result = translator.translate_text(text, target_lang=target_locale.upper())
    return TranslationResult(
        provider="DeepL API",
        target_language=target_locale,
        translated_text=result.text,
        detected_source_language=getattr(result, "detected_source_lang", None),
    ).to_dict()
