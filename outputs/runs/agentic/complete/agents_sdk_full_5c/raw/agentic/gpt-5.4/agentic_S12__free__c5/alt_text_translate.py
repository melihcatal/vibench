from __future__ import annotations

import os

from deepl import DeepLClient


DEEPL_FORMALITY = os.getenv("DEEPL_FORMALITY", "prefer_less")


def alt_text_translate(text: str, target_lang: str = "DE") -> str:
    client = DeepLClient(os.getenv("DEEPL_AUTH_KEY", ""))
    result = client.translate_text(text, target_lang=target_lang, formality=DEEPL_FORMALITY)
    return result.text.strip()
