from __future__ import annotations

from translation_client import get_client
from translation_models import TranslationRequest


def translate_markup(markup: str, source_language: str, target_language: str):
    client = get_client()
    return client.translate(
        TranslationRequest(
            text=markup,
            source_language=source_language,
            target_language=target_language,
            preserve_tags=True,
            format_type="html",
        )
    )
