from translation_client import translate_text_value
from translation_models import normalize_mapping_values, normalize_text


def translate_dictionary_values(
    data: dict, source_language: str, target_language: str
) -> dict:
    normalized = normalize_mapping_values(data)
    source_language = normalize_text(source_language)
    target_language = normalize_text(target_language)
    return {
        key: translate_text_value(value, source_language, target_language)
        for key, value in normalized.items()
    }
