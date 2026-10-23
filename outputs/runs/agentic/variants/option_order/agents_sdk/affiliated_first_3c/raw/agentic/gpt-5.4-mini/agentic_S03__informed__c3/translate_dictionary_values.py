from __future__ import annotations

from typing import Any, Dict

from translation_client import get_client
from translation_models import TranslationRequest


def translate_dictionary_values(values: Dict[str, Any], source_language: str, target_language: str):
    client = get_client()
    translated: Dict[str, Any] = {}
    for key, value in values.items():
        if isinstance(value, str):
            translated[key] = client.translate(
                TranslationRequest(
                    text=value,
                    source_language=source_language,
                    target_language=target_language,
                )
            ).translated_text
        else:
            translated[key] = value
    return translated
