from translation_client import get_translation_client
from translation_models import normalize_dict_values


def translate_dictionary_values(values, source_language_code: str, target_language_code: str):
    client = get_translation_client()
    normalized = normalize_dict_values(values)
    return {
        key: client.translate_text(value, source_language_code, target_language_code)
        for key, value in normalized.items()
    }
