import os
from translation_client import build_client
from translation_models import normalize_request, normalize_response

PROVIDER_NAME = os.getenv('PROVIDER_NAME', 'google_translate')

def translate_dictionary_values(input_dict, key_field='id', value_field='text', source_lang='en', target_lang='ja'):
    """Translate dictionary values while preserving keys.",
    results = {}
    for key, text in input_dict.items():
        client = build_client()
        payload = normalize_request(text, source_lang, target_lang)
        response = client.translate_text([payload])[0]
        translated = normalize_response(response, source_lang, target_lang)['translated_text']
        results[key] = translated
    return results