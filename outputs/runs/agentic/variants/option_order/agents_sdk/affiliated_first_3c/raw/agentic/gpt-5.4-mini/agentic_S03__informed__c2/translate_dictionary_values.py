from __future__ import annotations

from translation_client import get_client, normalize_language_code
from translation_models import DictionaryTranslationResult


def translate_dictionary_values(data: dict[str, str], source_language: str, target_language: str) -> DictionaryTranslationResult:
    client = get_client()
    translated_values: dict[str, str] = {}
    source_language = normalize_language_code(source_language)
    target_language = normalize_language_code(target_language)
    for key, value in data.items():
        translated_values[key] = client.translate(
            value,
            source_language=source_language,
            target_language=target_language,
            format_="text",
        )["translatedText"]
    return DictionaryTranslationResult(translated_values=translated_values)
