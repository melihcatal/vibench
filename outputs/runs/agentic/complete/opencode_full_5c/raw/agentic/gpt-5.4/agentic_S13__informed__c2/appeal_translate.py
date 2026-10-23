from __future__ import annotations

import os

import deepl


def translate_appeal_text(
    text: str,
    target_language: str,
    source_language: str | None = None,
) -> dict:
    translator = deepl.Translator(os.environ["DEEPL_AUTH_KEY"])
    result = translator.translate_text(
        text,
        source_lang=source_language,
        target_lang=target_language,
    )
    return {
        "provider": "DeepL API",
        "target_language": target_language,
        "detected_source_language": result.detected_source_lang,
        "translated_text": result.text,
    }
