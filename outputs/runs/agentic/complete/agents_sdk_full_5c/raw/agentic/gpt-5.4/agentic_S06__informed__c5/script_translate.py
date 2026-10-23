from __future__ import annotations

import os
from typing import Optional

import deepl

from speech_models import TranslationResult


DEEPL_MODEL_TYPE = "quality_optimized"


def translate_script(text: str, target_language: str, source_language: Optional[str] = None) -> TranslationResult:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("Missing DEEPL_AUTH_KEY")

    translator = deepl.Translator(auth_key)
    result = translator.translate_text(
        text,
        source_lang=source_language,
        target_lang=target_language,
        model_type=DEEPL_MODEL_TYPE,
    )
    return TranslationResult(
        translated_text=result.text,
        detected_source_language=getattr(result, "detected_source_lang", source_language),
        target_language=target_language,
        provider="DeepL",
    )
