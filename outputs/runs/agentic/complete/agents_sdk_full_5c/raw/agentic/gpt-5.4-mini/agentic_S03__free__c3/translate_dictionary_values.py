from translation_client import TranslationClient
from translation_models import normalize_dictionary_values

PROVIDER = "GoogleTranslator"


def translate_dictionary_values(data, source_language: str = "auto", target_language: str = "en"):
    normalized = normalize_dictionary_values(data)
    client = TranslationClient()
    return {
        key: client.translate(value, source_language, target_language)
        for key, value in normalized.items()
    }
