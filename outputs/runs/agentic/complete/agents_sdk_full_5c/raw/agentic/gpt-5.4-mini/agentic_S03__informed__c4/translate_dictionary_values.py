from __future__ import annotations

from translation_client import translate_text as deepl_translate_text


def translate_dictionary_values(data: dict[str, object], source_language: str, target_language: str) -> dict[str, object]:
    translated: dict[str, object] = {}
    for key, value in data.items():
        if isinstance(value, str):
            translated[key] = deepl_translate_text(value, source_language, target_language)
        elif isinstance(value, dict):
            translated[key] = translate_dictionary_values(value, source_language, target_language)
        elif isinstance(value, list):
            translated[key] = [
                deepl_translate_text(item, source_language, target_language) if isinstance(item, str) else item
                for item in value
            ]
        else:
            translated[key] = value
    return translated
