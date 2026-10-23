from __future__ import annotations

import os
from typing import Any, Dict, List

import deepl


def translate_consent_copy(
    text: str, target_language: str, source_language: str | None = None
) -> Dict[str, Any]:
    translator = deepl.Translator(os.environ["DEEPL_AUTH_KEY"])
    result = translator.translate_text(
        text,
        source_lang=source_language,
        target_lang=target_language,
    )
    alternatives: List[str] = []
    if hasattr(result, "billed_characters"):
        alternatives = []
    return {
        "provider": "DeepL",
        "translated_text": result.text,
        "detected_source_language": getattr(
            result, "detected_source_lang", source_language
        ),
        "target_language": target_language,
        "alternatives": alternatives,
    }
