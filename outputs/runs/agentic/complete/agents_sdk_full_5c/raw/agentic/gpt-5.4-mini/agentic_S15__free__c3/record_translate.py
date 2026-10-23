from __future__ import annotations

from typing import Any, Dict

from database_models import TranslationResult


GOOGLE_TRANSLATE_HOST = "translation.googleapis.com"


def translate_record_fields(record: Dict[str, Any], target_language: str) -> TranslationResult:
    translated = {}
    for key in ("title", "description", "content"):
        if key in record and record[key] is not None:
            translated[key] = f"[{target_language}] {record[key]}"
    return TranslationResult(document_id=str(record.get("document_id", "")), translated_fields=translated, target_language=target_language)
