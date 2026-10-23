from __future__ import annotations

from typing import Any, Dict, Mapping

from translation_client import get_client
from translation_models import normalize_dict_values

PROVIDER = "azure-ai-translation-text"


def translate_dictionary_values(data: Mapping[str, Any], source_language: str, target_language: str) -> Dict[str, str]:
    client = get_client()
    normalized = normalize_dict_values(data)
    values = list(normalized.values())
    results = client.translate(body=values, to_language=[target_language], from_parameter=source_language or None)
    translated_values = [item.translations[0].text if item.translations else values[idx] for idx, item in enumerate(results)]
    return {key: translated_values[idx] for idx, key in enumerate(normalized.keys())}
