from __future__ import annotations

from typing import Dict

from translation_client import get_azure_translator_client
from translation_models import normalize_mapping_values


def translate_dictionary_values(source_language: str, target_language: str, values: Dict[str, str]) -> Dict[str, str]:
    client = get_azure_translator_client()
    normalized = normalize_mapping_values(values)
    keys = list(normalized.keys())
    texts = list(normalized.values())
    response = client.translate(body=texts, from_parameter=source_language, to=[target_language])
    translated_values = [item.translations[0].text if item.translations else "" for item in response]
    return dict(zip(keys, translated_values))
