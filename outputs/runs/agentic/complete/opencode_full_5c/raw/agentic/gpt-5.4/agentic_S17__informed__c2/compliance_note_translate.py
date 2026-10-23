from __future__ import annotations

import os
from typing import Dict, Optional

import deepl

from security_models import TranslationResult


def compliance_note_translate(
    text: str, target_language: str, source_language: Optional[str] = None
) -> Dict[str, object]:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("Missing DEEPL_AUTH_KEY")
    translator = deepl.Translator(auth_key)
    translation = translator.translate_text(
        text,
        target_lang=target_language,
        source_lang=source_language,
        model_type="quality_optimized",
    )
    result = TranslationResult(
        provider="deepl",
        source_language=source_language
        or getattr(translation, "detected_source_lang", None),
        target_language=target_language,
        translated_text=translation.text,
        model="quality_optimized",
    )
    return result.to_dict()
