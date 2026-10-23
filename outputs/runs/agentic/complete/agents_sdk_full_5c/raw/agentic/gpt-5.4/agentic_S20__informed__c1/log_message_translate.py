from __future__ import annotations

import os
from typing import Dict

import deepl


DEEPL_MODEL_TYPE = "quality_optimized"


def log_message_translate(text: str, target_lang: str, source_lang: str | None = None) -> Dict[str, str]:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY is required")
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(
        text,
        source_lang=source_lang,
        target_lang=target_lang,
        model_type=DEEPL_MODEL_TYPE,
    )
    return {
        "provider": "DeepL",
        "translated_text": result.text,
        "detected_source_lang": getattr(result, "detected_source_lang", source_lang or ""),
        "target_lang": target_lang,
    }
