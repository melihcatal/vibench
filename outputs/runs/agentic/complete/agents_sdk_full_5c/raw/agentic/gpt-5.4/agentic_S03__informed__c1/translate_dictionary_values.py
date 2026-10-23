from __future__ import annotations

from typing import Any, Dict, Optional

from translation_client import get_translation_client
from translation_models import normalize_string_mapping


def translate_dictionary_values(
    values: Dict[str, Any],
    target_language: str,
    source_language: Optional[str] = None,
) -> Dict[str, str]:
    client = get_translation_client()
    normalized = normalize_string_mapping(values)
    keys = list(normalized.keys())
    translated = client.translate_batch(
        [normalized[key] for key in keys],
        target_language=target_language,
        source_language=source_language,
        preserve_formatting=True,
    )
    return {key: translated[index].text for index, key in enumerate(keys)}
