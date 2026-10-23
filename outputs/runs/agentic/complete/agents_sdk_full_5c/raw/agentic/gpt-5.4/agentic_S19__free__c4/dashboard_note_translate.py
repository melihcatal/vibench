from __future__ import annotations

import os
from typing import Dict

from deepl import Translator


DEEPL_TARGET_DEFAULT = "DE"


def dashboard_note_translate(text: str, target_lang: str = DEEPL_TARGET_DEFAULT, source_lang: str | None = None) -> Dict[str, str]:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY is required.")
    translator = Translator(auth_key)
    result = translator.translate_text(text, target_lang=target_lang, source_lang=source_lang)
    return {
        "provider": "DeepL",
        "target_lang": target_lang,
        "detected_source_lang": result.detected_source_lang,
        "text": result.text,
    }
