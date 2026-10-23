from __future__ import annotations

from typing import Mapping, Dict

from translation_client import translate_text as deepl_translate_text
from translation_models import preserve_mapping_keys, TranslationResult


def translate_dictionary_values(data: Mapping[str, str], source_language: str, target_language: str) -> Dict[str, str]:
    preserved = preserve_mapping_keys(data)
    translated: Dict[str, str] = {}
    for key, value in preserved.items():
        translated[key] = deepl_translate_text(value, source_language, target_language)["translated_text"]
    return translated
