from __future__ import annotations

import os

from deepl import DeepLClient


def log_message_translate(
    message: str, target_lang: str, source_lang: str | None = None
) -> dict:
    client = DeepLClient(os.environ["DEEPL_API_KEY"])
    response = client.translate_text(
        message, target_lang=target_lang, source_lang=source_lang
    )
    return {
        "provider": "DeepL",
        "target_lang": target_lang,
        "detected_source_lang": response.detected_source_lang,
        "translated_text": response.text,
    }
