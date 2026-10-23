from __future__ import annotations

from translation_client import TranslationClient
from translation_models import TranslationRequest

_client = TranslationClient()


def translate_text(text: str, source_language: str, target_language: str) -> str:
    result = _client.translate(TranslationRequest(source_language=source_language, target_language=target_language, text=text))
    return result.translated_text
