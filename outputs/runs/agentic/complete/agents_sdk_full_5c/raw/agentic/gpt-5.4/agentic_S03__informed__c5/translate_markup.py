from __future__ import annotations

from typing import Optional

from translation_client import get_translation_client
from translation_models import TranslationRequest, TranslationResult


def translate_markup(
    markup: str,
    target_language: str,
    source_language: Optional[str] = None,
) -> TranslationResult:
    client = get_translation_client()
    request = TranslationRequest(
        text=markup,
        source_language=source_language,
        target_language=target_language,
        text_type="html",
        preserve_formatting=True,
    )
    return client.translate_text(request)
