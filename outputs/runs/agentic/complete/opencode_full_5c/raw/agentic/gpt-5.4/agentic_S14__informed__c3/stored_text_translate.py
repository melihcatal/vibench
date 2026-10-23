from __future__ import annotations

import deepl

from storage_client import require_deepl_auth_key
from storage_models import TranslationResult


def translate_extracted_text(
    text: str, target_language: str, source_language: str | None = None
) -> TranslationResult:
    translator = deepl.Translator(require_deepl_auth_key())
    result = translator.translate_text(
        text, target_lang=target_language, source_lang=source_language
    )
    detected = getattr(result, "detected_source_lang", None) or source_language
    return TranslationResult(
        source_language=detected,
        target_language=target_language,
        translated_text=result.text,
    )
