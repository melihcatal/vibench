from __future__ import annotations

import os

import deepl

from messaging_models import TranslationResult


DEEPL_MODEL = "DeepL API"


def translate_payload_text(
    source_message_id: str, text: str, target_language: str, source_language: str = "EN"
) -> TranslationResult:
    translator = deepl.Translator(os.getenv("DEEPL_AUTH_KEY"))
    result = translator.translate_text(
        text, source_lang=source_language, target_lang=target_language
    )
    return TranslationResult(
        provider=DEEPL_MODEL,
        source_message_id=source_message_id,
        source_language=source_language,
        target_language=target_language,
        translated_text=result.text,
    )
