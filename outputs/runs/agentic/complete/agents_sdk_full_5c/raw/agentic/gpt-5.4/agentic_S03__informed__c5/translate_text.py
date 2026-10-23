from __future__ import annotations

from typing import Optional

from translation_client import get_translation_client
from translation_models import TranslationRequest, TranslationResult


def translate_text(
    text: str,
    target_language: str,
    source_language: Optional[str] = None,
    glossary_id: Optional[str] = None,
    formality: Optional[str] = None,
) -> TranslationResult:
    client = get_translation_client()
    request = TranslationRequest(
        text=text,
        source_language=source_language,
        target_language=target_language,
        glossary_id=glossary_id,
        formality=formality,
        text_type="plain",
    )
    return client.translate_text(request)
