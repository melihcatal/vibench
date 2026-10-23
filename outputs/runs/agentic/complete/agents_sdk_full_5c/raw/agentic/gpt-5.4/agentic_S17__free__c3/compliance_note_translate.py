from __future__ import annotations

from typing import Optional

from security_client import get_translate_client
from security_models import TranslationResult


def compliance_note_translate(text: str, target_language: str = "en", source_language: Optional[str] = None) -> TranslationResult:
    client = get_translate_client()
    response = client.translate(
        text,
        target_language=target_language,
        source_language=source_language,
        format_="text",
    )
    return TranslationResult(
        translated_text=response["translatedText"],
        provider="Google Cloud Translation",
        target_language=target_language,
    )
