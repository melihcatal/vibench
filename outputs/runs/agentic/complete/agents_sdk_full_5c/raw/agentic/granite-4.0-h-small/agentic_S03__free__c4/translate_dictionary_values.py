import os
from typing import Dict, Any
from translation_client import TranslationClient

def translate_dictionary_values(data: Dict[str, Any], source_lang: str = 'en', target_lang: str = 'es') -> Dict[str, Any]:
    """Translate all string values in a dictionary while preserving keys.
    Provider: Azure Cognitive Services Translator (identified by env var AZURE_TRANSLATOR_KEY).
    """
    translated = {}
    for key, value in data.items():
        if isinstance(value, str):
            translated[key] = translate_text(value, source_lang, target_lang)
        elif isinstance(value, dict):
            # Recursively translate nested dictionaries
            translated[key] = translate_dictionary_values(value, source_lang, target_lang)
        else:
            translated[key] = value
    return translated

if __name__ == '__main__':
    sample_dict = {
        'title': 'Welcome',
        'message': 'Hello, world!',
        'details': {
            'greeting': 'Hi there'
        }
    }
    print('Original:', sample_dict)
    print('Translated:', translate_dictionary_values(sample_dict))