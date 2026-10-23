from __future__ import annotations

import os

import deepl


def translate_query(
    query: str, target_language: str, source_language: str | None = None
) -> dict[str, str]:
    translator = deepl.Translator(os.environ["DEEPL_AUTH_KEY"])
    result = translator.translate_text(
        query, target_lang=target_language, source_lang=source_language
    )
    detected = source_language or getattr(result, "detected_source_lang", "")
    return {
        "provider": "DeepL",
        "translated_text": result.text,
        "target_language": target_language,
        "detected_source_language": detected,
    }
