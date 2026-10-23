from __future__ import annotations

from typing import Any, Dict

from translation_client import translate_dictionary_values as _translate_dictionary_values


def translate_dictionary_values(values: Dict[str, Any], source_language: str, target_language: str) -> Dict[str, str]:
    return _translate_dictionary_values(values, source_language, target_language)
