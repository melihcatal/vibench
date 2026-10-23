from __future__ import annotations

import os

import deepl


def alt_text_translate(
    text: str, target_language: str, source_language: str | None = None
) -> dict:
    client = deepl.Translator(os.getenv("DEEPL_AUTH_KEY"))
    result = client.translate_text(
        text, target_lang=target_language, source_lang=source_language
    )
    return {
        "provider": "deepl-api",
        "translated_text": result.text,
        "detected_source_language": result.detected_source_lang,
        "target_language": target_language,
    }
