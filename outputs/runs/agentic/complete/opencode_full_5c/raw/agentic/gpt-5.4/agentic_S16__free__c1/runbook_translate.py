from __future__ import annotations

import os

from deepl import DeepLClient


def translate_runbook_notes(
    text: str, target_language: str, source_language: str | None = None
) -> dict:
    auth_key = os.getenv("DEEPL_API_KEY")
    if not auth_key:
        raise ValueError("Missing DEEPL_API_KEY")
    client = DeepLClient(auth_key)
    result = client.translate_text(
        text,
        source_lang=source_language,
        target_lang=target_language,
        model_type="quality_optimized",
    )
    return {
        "provider": "deepl",
        "target_language": target_language,
        "detected_source_language": result.detected_source_lang,
        "translation": result.text,
    }
