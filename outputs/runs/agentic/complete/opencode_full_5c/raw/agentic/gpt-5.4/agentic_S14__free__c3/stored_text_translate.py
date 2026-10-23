from __future__ import annotations

from storage_client import get_translate_client, get_translate_parent
from storage_models import TranslationResult


def translate_extracted_text(
    text: str, target_language: str, source_language: str | None = None
) -> TranslationResult:
    client = get_translate_client()
    response = client.translate_text(
        request={
            "parent": get_translate_parent(),
            "contents": [text],
            "mime_type": "text/plain",
            "target_language_code": target_language,
            "source_language_code": source_language,
        }
    )
    translated_text = (
        response.translations[0].translated_text if response.translations else ""
    )
    return TranslationResult(
        source_text=text,
        translated_text=translated_text,
        target_language=target_language,
    )
