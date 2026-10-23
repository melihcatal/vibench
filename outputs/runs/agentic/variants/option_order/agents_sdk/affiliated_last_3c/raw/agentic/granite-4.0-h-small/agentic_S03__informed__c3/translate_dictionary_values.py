import os
from google.cloud import translate_v2 as translate

# Helpers from local modules
from translation_client import get_translation_client
from translation_models import validate_text, validate_language_code

def translate_dictionary_values(dictionary: dict, target_lang: str) -> dict:
    """Translates all string values in a dictionary while preserving keys.

    Args:
        dictionary: Input mapping with string values to translate.
        target_lang: Target language code (e.g., "es", "fr").

    Returns:
        New dict with original keys and translated string values.
    """
    client = get_translation_client()
    validate_language_code(target_lang)
    translated = {}
    for key, value in dictionary.items():
        if isinstance(value, str):
            translated[key] = client.translate(value, target_language=target_lang)['translatedText']
        else:
            # Non-string values are kept unchanged
            translated[key] = value
    return translated

if __name__ == "__main__":
    sample = {
        "welcome": "Welcome",
        "farewell": "Goodbye"
    }
    target = "es"
    print("Original:", sample)
    print("Translated:", translate_dictionary_values(sample, target))