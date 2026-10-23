from __future__ import annotations

import os
from typing import Optional

import deepl


PROVIDER = "deepl"


def translate_alt_text(text: str, target_language: str, source_language: Optional[str] = None) -> dict:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise EnvironmentError("DEEPL_AUTH_KEY is required for DeepL API")

    translator = deepl.Translator(auth_key)
    result = translator.translate_text(
        text,
        target_lang=target_language.upper(),
        source_lang=source_language.upper() if source_language else None,
        preserve_formatting=True,
    )
    return {
        "provider": PROVIDER,
        "target_language": target_language.upper(),
        "translated_text": result.text,
        "detected_source_language": result.detected_source_lang,
    }
