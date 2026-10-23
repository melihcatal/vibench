from translation_client import get_default_source_language, get_default_target_language, get_translation_client
from translation_models import normalize_mapping_values


def translate_dictionary_values(values, source_language=None, target_language=None):
    normalized = normalize_mapping_values(values)
    client = get_translation_client()
    source_language = source_language or get_default_source_language()
    target_language = target_language or get_default_target_language()
    translated = {}
    for key, value in normalized.items():
        translated[key] = client.translate(value, source_language=source_language, target_language=target_language)["translatedText"]
    return translated
