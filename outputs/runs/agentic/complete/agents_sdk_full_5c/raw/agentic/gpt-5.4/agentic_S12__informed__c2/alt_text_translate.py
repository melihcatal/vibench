from __future__ import annotations

import os
from typing import Dict, Any

import deepl

DEEPL_PROVIDER = "deepl"


def alt_text_translate(text: str, target_language: str, source_language: str | None = None) -> Dict[str, Any]:
    translator = deepl.Translator(os.environ["DEEPL_AUTH_KEY"])
    result = translator.translate_text(
        text,
        target_lang=target_language.upper(),
        source_lang=source_language.upper() if source_language else None,
        preserve_formatting=True,
    )
    return {
        "provider": DEEPL_PROVIDER,
        "model": "DeepL API v2",
        "translated_text": result.text,
        "detected_source_language": result.detected_source_lang,
        "target_language": target_language.upper(),
    }
