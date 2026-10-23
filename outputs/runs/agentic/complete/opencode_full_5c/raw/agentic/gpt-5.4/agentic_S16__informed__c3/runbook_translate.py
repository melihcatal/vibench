from __future__ import annotations

from security_client import translate_text
from security_models import TranslationResult, normalize_translation


def runbook_translate(text: str, target_language: str) -> dict:
    result = translate_text(text, target_language=target_language)
    payload = TranslationResult(
        source_text=text,
        translated_text=result["text"],
        target_language=target_language,
        detected_source_language=result.get("detected_source_lang"),
    )
    return normalize_translation(payload)
