import os
from typing import Any, Mapping

from translation_client import get_translation_client
from translation_models import DictionaryTranslationRequest, DictionaryTranslationResult


DEFAULT_SOURCE_LANG = os.getenv("TRANSLATION_SOURCE_LANG", "auto")
DEFAULT_TARGET_LANG = os.getenv("TRANSLATION_TARGET_LANG", "en")


def translate_dictionary_values(data: Mapping[str, Any], source_language: str = None, target_language: str = None) -> DictionaryTranslationResult:
    client = get_translation_client()
    request = DictionaryTranslationRequest(
        data=dict(data),
        source_language=source_language or DEFAULT_SOURCE_LANG,
        target_language=target_language or DEFAULT_TARGET_LANG,
    )
    return client.translate_dictionary_values(request)


__all__ = ["translate_dictionary_values"]
