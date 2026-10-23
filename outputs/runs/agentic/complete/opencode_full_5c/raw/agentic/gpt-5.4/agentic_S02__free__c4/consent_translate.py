from __future__ import annotations

import os

from deepl import DeepLClient


def consent_translate(
    text: str, target_language: str, source_language: str | None = None
) -> dict:
    client = DeepLClient(os.environ["DEEPL_API_KEY"])
    result = client.translate_text(
        text,
        target_lang=target_language,
        source_lang=source_language,
        model_type="prefer_quality_optimized",
    )
    return {
        "provider": "deepl",
        "text": result.text,
        "detected_source_language": result.detected_source_lang,
        "target_language": target_language,
    }
