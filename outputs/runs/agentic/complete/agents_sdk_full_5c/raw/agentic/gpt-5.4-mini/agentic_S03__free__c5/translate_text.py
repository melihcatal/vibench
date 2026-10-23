import os
from typing import Optional

from translation_client import TranslationServiceClient, get_translation_client
from translation_models import TranslationRequest, TranslationResult, normalize_text


DEFAULT_SOURCE_LANG = os.getenv("TRANSLATION_SOURCE_LANG", "auto")
DEFAULT_TARGET_LANG = os.getenv("TRANSLATION_TARGET_LANG", "en")


def translate_text(text: str, source_language: Optional[str] = None, target_language: Optional[str] = None) -> TranslationResult:
    client = get_translation_client()
    request = TranslationRequest(
        text=normalize_text(text),
        source_language=source_language or DEFAULT_SOURCE_LANG,
        target_language=target_language or DEFAULT_TARGET_LANG,
    )
    return client.translate_text(request)


__all__ = ["translate_text", "TranslationServiceClient"]
