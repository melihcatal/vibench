from translation_models import normalize_mapping_values
from translate_text import translate_text


def translate_dictionary_values(data, source_language=None, target_language="en"):
    normalized = normalize_mapping_values(data)
    return {key: translate_text(value, source_language=source_language, target_language=target_language).translated_text for key, value in normalized.items()}
