from translation_client import create_translation_client
from translation_models import normalize_dictionary_values


def translate_dictionary_values(data, source_language=None, target_language="en"):
    client = create_translation_client()
    normalized = normalize_dictionary_values(data)
    keys = list(normalized.keys())
    values = list(normalized.values())
    translated = client.translate_text(
        values, source_lang=source_language, target_lang=target_language
    )
    return {key: item.text for key, item in zip(keys, translated)}
