from __future__ import annotations

import deepl

from messaging_models import extract_text


def translate_payload_text(
    payload: dict, target_language: str, source_language: str | None = None
) -> dict[str, str]:
    client = deepl.Translator()
    text = extract_text(payload)
    result = client.translate_text(
        text, target_lang=target_language, source_lang=source_language
    )
    return {
        "translated_text": result.text,
        "detected_source_language": result.detected_source_lang,
        "provider": "DeepL",
    }
