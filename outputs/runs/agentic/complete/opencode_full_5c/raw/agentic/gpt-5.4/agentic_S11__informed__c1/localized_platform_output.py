from __future__ import annotations

import os
from typing import Any, Dict

import deepl


def localize_platform_output(text: str, target_locale: str) -> Dict[str, Any]:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("Missing required environment variable: DEEPL_AUTH_KEY")
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(text, target_lang=target_locale)
    return {
        "provider": "deepl",
        "target_locale": target_locale,
        "text": result.text,
        "detected_source_language": result.detected_source_lang,
        "billed_characters": getattr(result, "billed_characters", None),
        "raw": result,
    }
