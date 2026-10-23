from __future__ import annotations

import deepl


def translate_payload_text(
    text: str, target_language: str, source_language: str | None = None
) -> dict:
    auth_key = __import__("os").getenv("DEEPL_AUTH_KEY")
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(
        text, target_lang=target_language, source_lang=source_language
    )
    return {
        "provider": "deepl",
        "target_language": target_language,
        "detected_source_language": result.detected_source_lang,
        "translated_text": result.text,
    }
