from __future__ import annotations

from typing import Optional

from translation_client import get_translation_client
from translation_models import TranslationRequest, TranslationResult, normalize_text


def translate_text(
    text: str,
    target_language: str,
    source_language: Optional[str] = None,
) -> TranslationResult:
    client = get_translation_client()
    request = TranslationRequest(
        text=normalize_text(text),
        source_language=source_language,
        target_language=target_language,
    )
    return client.translate_text(
        request.text,
        target_language=request.target_language,
        source_language=request.source_language,
    )
