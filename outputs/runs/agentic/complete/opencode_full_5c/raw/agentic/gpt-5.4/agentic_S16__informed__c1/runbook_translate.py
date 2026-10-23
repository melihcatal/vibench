from __future__ import annotations

from security_client import get_deepl_translator
from security_models import TranslationResult


def translate_runbook_notes(
    text: str, target_language: str, source_language: str | None = None
) -> TranslationResult:
    translator = get_deepl_translator()
    result = translator.translate_text(
        text, target_lang=target_language, source_lang=source_language
    )
    detected_source = source_language or getattr(result, "detected_source_lang", None)
    return TranslationResult(
        source_language=detected_source,
        target_language=target_language,
        translated_text=result.text,
        provider="deepl",
    )
