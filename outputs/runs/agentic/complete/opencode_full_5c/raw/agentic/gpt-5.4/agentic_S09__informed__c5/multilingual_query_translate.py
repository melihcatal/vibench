from __future__ import annotations

import os

import deepl


def translate_query(
    text: str, target_language: str, source_language: str | None = None
) -> dict:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise EnvironmentError("DEEPL_AUTH_KEY is required")
    client = deepl.Translator(auth_key)
    result = client.translate_text(
        text,
        target_lang=target_language.upper(),
        source_lang=source_language.upper() if source_language else None,
    )
    return {
        "provider": "deepl",
        "target_language": target_language.upper(),
        "source_language": result.detected_source_lang,
        "translation": result.text,
    }
