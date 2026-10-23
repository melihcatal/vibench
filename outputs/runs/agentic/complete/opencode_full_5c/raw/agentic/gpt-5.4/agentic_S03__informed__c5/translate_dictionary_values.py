from __future__ import annotations

from typing import Any, Dict, Mapping

from translation_client import translate_text_items
from translation_models import normalize_mapping_values


def translate_dictionary_values(
    data: Mapping[str, Any], source_language: str | None, target_language: str
) -> Dict[str, str]:
    normalized = normalize_mapping_values(data)
    keys = list(normalized.keys())
    values = [normalized[key] for key in keys]
    result = translate_text_items(
        values, target_language=target_language, source_language=source_language
    )
    return {key: result.translations[index].text for index, key in enumerate(keys)}
