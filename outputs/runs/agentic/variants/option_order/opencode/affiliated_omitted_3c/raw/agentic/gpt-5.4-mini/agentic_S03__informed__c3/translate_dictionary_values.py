from translation_client import get_client
from translation_models import normalize_dict_values


def translate_dictionary_values(data, source_lang: str, target_lang: str):
    client = get_client()
    normalized = normalize_dict_values(data)
    translated = {}
    for key, value in normalized.items():
        translated[key] = client.translate_text(value, source_lang=source_lang, target_lang=target_lang).text
    return translated
