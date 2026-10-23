from translation_client import create_translation_client, target_language_code
from translation_models import TranslationResponse, normalize_mapping_values


def translate_dictionary_values(source_language: str, target_language: str, values: dict[str, object]) -> dict[str, str]:
    client = create_translation_client()
    normalized = normalize_mapping_values(values)
    translated: dict[str, str] = {}
    for key, value in normalized.items():
        result = client.translate_text(value, source_lang=target_language_code(source_language), target_lang=target_language_code(target_language))
        translated[key] = result.text
    return translated
