from __future__ import annotations

import os

import deepl

from vision_models import TranslationResult


DEEPL_PROVIDER = "deepl"


def translate_alt_text(text: str, target_language: str) -> TranslationResult:
    translator = deepl.Translator(os.environ["DEEPL_AUTH_KEY"])
    result = translator.translate_text(text, target_lang=target_language)
    return TranslationResult(
        translated_text=result.text,
        target_language=target_language,
        provider=DEEPL_PROVIDER,
    )
