import os
from typing import Dict, Any
from translation_client import get_translation_client
from translation_models import TranslationRequest, TranslationResponse

def translate_dictionary_values(data: Dict[str, Any], source_lang: str = 'en', target_lang: str = 'fr') -> Dict[str, Any]:
    """Translate the string values of a dictionary while preserving keys.
    Uses IBM Watson Language Translator as the concrete provider.
    The provider is identified by model_id (e.g., 'en-fr') and configured via WATSONX_API_KEY.
    Nested dictionaries are processed recursively.
    """
    client = get_translation_client()
    def _translate_value(val):
        if isinstance(val, str):
            request = TranslationRequest(text=val, source=source_lang, target=target_lang)
            response = client.translate(request)
            return response.translated_text
        elif isinstance(val, dict):
            return translate_dictionary_values(val, source_lang, target_lang)
        # other types (list, int, etc.) are left unchanged
        return val
    translated = {k: _translate_value(v) for k, v in data.items()}
    return translated

if __name__ == '__main__':
    sample_dict = {
        'title': 'Welcome to the site',
        'description': 'This is a multilingual demo.',
        'nested': {
            'greeting': 'Hello, world!'
        }
    }
    translated_dict = translate_dictionary_values(sample_dict, source_lang='en', target_lang='pt')
    print('Original dict:', sample_dict)
    print('Translated dict:', translated_dict)
