from __future__ import annotations

import os
from typing import Any

import deepl


def appeal_translate(
    text: str, target_language: str, source_language: str | None = None
) -> dict[str, Any]:
    client = deepl.Translator(os.environ["DEEPL_AUTH_KEY"])
    result = client.translate_text(
        text, target_lang=target_language, source_lang=source_language
    )
    return {
        "provider": "deepl",
        "text": text,
        "translated_text": result.text,
        "detected_source_language": result.detected_source_lang,
        "target_language": target_language,
    }
