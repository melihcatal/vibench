from __future__ import annotations

from typing import Mapping, Any

from translation_client import TranslationClient
from translation_models import TranslationRequest

_client = TranslationClient()


def translate_dictionary_values(data: Mapping[str, Any], source_language: str, target_language: str) -> dict[str, str]:
    translated: dict[str, str] = {}
    for key, value in data.items():
        translated[key] = _client.translate(TranslationRequest(source_language=source_language, target_language=target_language, text=str(value))).translated_text
    return translated
