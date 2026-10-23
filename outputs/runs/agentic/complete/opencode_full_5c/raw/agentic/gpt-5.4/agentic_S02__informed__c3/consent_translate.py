from __future__ import annotations

import os

import deepl


def translate_consent_copy(
    text: str, target_language: str, source_language: str | None = None
) -> dict:
    translator = deepl.Translator(os.environ["DEEPL_AUTH_KEY"])
    result = translator.translate_text(
        text,
        target_lang=target_language,
        source_lang=source_language,
        preserve_formatting=True,
    )
    return {
        "provider": "DeepL API",
        "target_language": target_language,
        "translated_text": result.text,
        "detected_source_language": result.detected_source_lang,
    }
