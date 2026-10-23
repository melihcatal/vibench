from __future__ import annotations

from typing import Any, Dict, Mapping

from translation_client import get_deepl_client
from translation_models import normalize_dictionary_values, normalize_language_code


def translate_dictionary_values(data: Mapping[str, Any], source_language: str | None, target_language: str) -> Dict[str, str]:
    normalized = normalize_dictionary_values(data)
    keys = list(normalized.keys())
    values = [normalized[key] for key in keys]
    client = get_deepl_client()
    responses = client.translate_text(
        values,
        source_lang=normalize_language_code(source_language),
        target_lang=normalize_language_code(target_language),
    )
    return {key: response.text for key, response in zip(keys, responses)}
