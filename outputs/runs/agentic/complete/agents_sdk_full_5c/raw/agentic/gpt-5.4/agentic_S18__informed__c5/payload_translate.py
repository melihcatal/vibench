from __future__ import annotations

import os
from typing import Dict, Optional

import deepl


DEEPL_MODEL_TYPE = "quality_optimized"


def translate_payload_text(text: str, target_lang: str, source_lang: Optional[str] = None) -> Dict[str, str]:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("Missing DEEPL_AUTH_KEY")
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(
        text,
        source_lang=source_lang,
        target_lang=target_lang,
        model_type=DEEPL_MODEL_TYPE,
    )
    detected = getattr(result, "detected_source_lang", None) or source_lang or "unknown"
    return {
        "provider": "deepl",
        "translated_text": result.text,
        "target_lang": target_lang,
        "detected_source_lang": detected,
    }
