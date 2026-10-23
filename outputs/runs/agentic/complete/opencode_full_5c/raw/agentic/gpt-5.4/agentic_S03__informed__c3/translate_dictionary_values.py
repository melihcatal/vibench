from __future__ import annotations

from typing import Any, Dict, Mapping

from translation_client import translate_texts_with_deepl
from translation_models import normalize_string_mapping


def translate_dictionary_values(
    values: Mapping[str, Any],
    target_language: str,
    source_language: str | None = None,
    formality: str | None = None,
) -> Dict[str, str]:
    normalized = normalize_string_mapping(values)
    keys = list(normalized.keys())
    translated = translate_texts_with_deepl(
        [normalized[key] for key in keys],
        source_language=source_language,
        target_language=target_language,
        formality=formality,
    )
    return {key: translated[index].text for index, key in enumerate(keys)}
