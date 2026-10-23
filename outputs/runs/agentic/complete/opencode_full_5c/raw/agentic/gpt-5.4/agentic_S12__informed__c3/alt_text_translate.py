from __future__ import annotations

import os

import deepl

from vision_models import TranslationResult


def translate_alt_text(text: str, target_language: str) -> dict:
    translator = deepl.Translator(os.environ["DEEPL_AUTH_KEY"])
    response = translator.translate_text(text, target_lang=target_language)
    result = TranslationResult(
        provider="deepl",
        target_language=target_language,
        translated_text=response.text,
        raw_response={"detected_source_language": response.detected_source_lang},
    )
    return result.to_dict()
