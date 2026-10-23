from __future__ import annotations

from typing import Optional

import deepl

from storage_client import get_deepl_auth_key
from storage_models import TranslationResult


def translate_extracted_text(text: str, target_language: str, source_language: Optional[str] = None) -> TranslationResult:
    translator = deepl.Translator(get_deepl_auth_key())
    result = translator.translate_text(text, target_lang=target_language, source_lang=source_language)
    detected_source = getattr(result, "detected_source_lang", None) or source_language
    return TranslationResult(
        text=result.text,
        source_language=detected_source,
        target_language=target_language,
    )
