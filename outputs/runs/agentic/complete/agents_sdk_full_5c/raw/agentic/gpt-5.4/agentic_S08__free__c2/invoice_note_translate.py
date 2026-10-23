from __future__ import annotations

import os

from deepl import DeepLClient


DEEPL_ENV = "DEEPL_AUTH_KEY"
TARGET_LANG = "EN-US"


def invoice_note_translate(text: str, target_lang: str = TARGET_LANG) -> dict:
    client = DeepLClient(os.environ.get(DEEPL_ENV))
    result = client.translate_text(text, target_lang=target_lang)
    return {
        "provider": "DeepL",
        "target_lang": target_lang,
        "detected_source_lang": result.detected_source_lang,
        "text": result.text,
        "billed_characters": getattr(result, "billed_characters", None),
    }
