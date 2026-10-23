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
        tag_handling="html",
    )
    return {
        "provider": "deepl",
        "translation": result.text,
        "detected_source_language": getattr(
            result, "detected_source_lang", source_language
        ),
        "target_language": target_language,
    }
