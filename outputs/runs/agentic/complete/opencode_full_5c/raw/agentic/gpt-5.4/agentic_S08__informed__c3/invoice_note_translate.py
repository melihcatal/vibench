from __future__ import annotations

import os
from typing import Dict

import deepl


def translate_invoice_note(
    text: str, target_language: str, source_language: str | None = None
) -> Dict[str, str]:
    translator = deepl.Translator(os.environ["DEEPL_AUTH_KEY"])
    result = translator.translate_text(
        text,
        source_lang=source_language,
        target_lang=target_language,
        model_type="prefer_quality_optimized",
    )
    return {
        "provider": "deepl-api",
        "text": result.text,
        "detected_source_language": result.detected_source_lang,
        "target_language": target_language,
    }
