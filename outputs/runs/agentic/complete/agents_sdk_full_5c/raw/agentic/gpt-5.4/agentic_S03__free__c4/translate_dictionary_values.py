from __future__ import annotations

from typing import Dict, Mapping, Optional

from batch_translate import batch_translate
from translation_models import normalize_dictionary_values


def translate_dictionary_values(data: Mapping[str, object], target_language: str, source_language: Optional[str] = None) -> Dict[str, str]:
    normalized = normalize_dictionary_values(data)
    keys = list(normalized.keys())
    values = [normalized[key] for key in keys]
    translated = batch_translate(values, target_language=target_language, source_language=source_language)
    return {key: translated[index].text for index, key in enumerate(keys)}
