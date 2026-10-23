from __future__ import annotations

import os

import deepl

from vision_models import TranslationResult


def alt_text_translate(text: str, target_language: str) -> dict:
    translator = deepl.Translator(os.environ["DEEPL_AUTH_KEY"])
    result = translator.translate_text(text, target_lang=target_language.upper())
    return TranslationResult(
        provider="deepl",
        translated_text=result.text,
        target_language=target_language.upper(),
    ).to_dict()
