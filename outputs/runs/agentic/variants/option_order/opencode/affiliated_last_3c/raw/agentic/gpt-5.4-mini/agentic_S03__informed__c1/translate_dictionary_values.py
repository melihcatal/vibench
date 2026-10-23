from typing import Dict

from translation_client import get_client


def translate_dictionary_values(values: Dict[str, str], source_language: str, target_language: str) -> Dict[str, str]:
    return get_client().translate_dictionary_values(values, source_language, target_language)
