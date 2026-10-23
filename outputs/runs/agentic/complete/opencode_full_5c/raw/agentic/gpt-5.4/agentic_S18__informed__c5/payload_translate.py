from __future__ import annotations

import os

import deepl


def translate_payload_text(
    text: str, target_language: str, source_language: str | None = None
) -> dict[str, str]:
    client = deepl.Translator(os.environ["DEEPL_AUTH_KEY"])
    result = client.translate_text(
        text, source_lang=source_language, target_lang=target_language
    )
    return {
        "provider": "deepl",
        "target_language": target_language,
        "text": result.text,
        "detected_source_language": result.detected_source_lang,
    }
