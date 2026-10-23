"""Translate dictionary values using DeepL while preserving keys."""

from __future__ import annotations

from typing import Any, Dict, Optional

import deepl

from translation_client import get_deepl_client, get_source_language, get_target_language
from translation_models import DictionaryTranslationRequest, DictionaryTranslationResponse, normalize_dictionary_values


def translate_dictionary_values(data: Dict[str, Any], source_lang: Optional[str] = None, target_lang: Optional[str] = None) -> Dict[str, Any]:
    request = DictionaryTranslationRequest(data=data, source_lang=source_lang, target_lang=target_lang)
    client = get_deepl_client()
    source = get_source_language(request.source_lang)
    target = get_target_language(request.target_lang)
    translated = {}
    for key, value in request.data.items():
        if isinstance(value, str):
            translated_value = client.translate_text(value, source_lang=source, target_lang=target).text
            translated[key] = translated_value
        else:
            translated[key] = value
    return normalize_dictionary_values(translated)


def translate_dictionary_values_response(data: Dict[str, Any], source_lang: Optional[str] = None, target_lang: Optional[str] = None) -> DictionaryTranslationResponse:
    translated_data = translate_dictionary_values(data, source_lang=source_lang, target_lang=target_lang)
    return DictionaryTranslationResponse(data=data, translated_data=translated_data, source_lang=source_lang, target_lang=target_lang)


__all__ = ["translate_dictionary_values", "translate_dictionary_values_response", "deepl"]
