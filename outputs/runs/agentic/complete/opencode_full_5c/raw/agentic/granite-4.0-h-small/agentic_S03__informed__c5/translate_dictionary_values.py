from translation_client import TranslationClient
from translation_models import parse_response

client = TranslationClient()


def translate_dictionary_values(data, target_lang):
    """Translate values of a dictionary while preserving keys.
    Assumes values are plain strings; nested structures are not handled.
    """
    translated = {}
    for key, text in data.items():
        raw = client.translate_text(text, target_lang)
        translated[key] = parse_response(raw)
    return translated
