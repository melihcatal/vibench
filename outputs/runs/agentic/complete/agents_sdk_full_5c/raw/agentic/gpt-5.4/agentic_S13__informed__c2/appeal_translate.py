from __future__ import annotations

import os
from typing import Dict, Optional

import deepl


def appeal_translate(
    text: str,
    target_language: str,
    source_language: Optional[str] = None,
    formality: str = "default",
) -> Dict[str, str]:
    translator = deepl.Translator(os.environ["DEEPL_AUTH_KEY"])
    result = translator.translate_text(
        text,
        target_lang=target_language,
        source_lang=source_language,
        formality=formality,
    )
    detected = source_language or (result.detected_source_lang or "")
    return {
        "provider": "DeepL API",
        "translated_text": result.text,
        "detected_source_language": detected,
        "target_language": target_language,
    }
