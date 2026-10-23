from translation_client import (
    translate_dictionary_values as _translate_dictionary_values,
)


def translate_dictionary_values(values, source_language: str, target_language: str):
    return _translate_dictionary_values(values, source_language, target_language)
