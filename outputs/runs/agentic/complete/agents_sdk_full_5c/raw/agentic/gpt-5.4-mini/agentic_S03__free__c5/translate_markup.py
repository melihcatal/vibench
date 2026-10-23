import os

from translation_client import get_translation_client
from translation_models import MarkupTranslationRequest, MarkupTranslationResult


DEFAULT_SOURCE_LANG = os.getenv("TRANSLATION_SOURCE_LANG", "auto")
DEFAULT_TARGET_LANG = os.getenv("TRANSLATION_TARGET_LANG", "en")


def translate_markup(markup: str, source_language: str = None, target_language: str = None) -> MarkupTranslationResult:
    client = get_translation_client()
    request = MarkupTranslationRequest(
        markup=markup,
        source_language=source_language or DEFAULT_SOURCE_LANG,
        target_language=target_language or DEFAULT_TARGET_LANG,
    )
    return client.translate_markup(request)


__all__ = ["translate_markup"]
