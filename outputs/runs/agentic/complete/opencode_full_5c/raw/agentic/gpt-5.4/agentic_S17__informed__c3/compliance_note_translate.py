from __future__ import annotations

from security_client import deepl_translator
from security_models import TranslationResult


def compliance_note_translate(text: str, target_language: str) -> TranslationResult:
    translator = deepl_translator()
    result = translator.translate_text(text, target_lang=target_language)
    return TranslationResult(
        provider="deepl",
        target_language=target_language,
        detected_source_language=result.detected_source_lang,
        translated_text=result.text,
    )
