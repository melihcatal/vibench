from __future__ import annotations

from typing import Any, Dict, List

import deepl


def translate_ocr_text(text: str, target_lang: str, source_lang: str | None = None, formality: str | None = None) -> Dict[str, Any]:
    auth_key = __import__("os").getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("Missing required environment variable: DEEPL_AUTH_KEY")
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(
        text,
        target_lang=target_lang,
        source_lang=source_lang,
        formality=formality,
    )
    alternatives: List[str] = []
    if hasattr(result, "billed_characters"):
        billed = result.billed_characters
    else:
        billed = None
    return {
        "provider": "deepl",
        "translated_text": result.text,
        "detected_source_lang": getattr(result, "detected_source_lang", source_lang),
        "target_lang": target_lang,
        "billed_characters": billed,
        "alternatives": alternatives,
    }
