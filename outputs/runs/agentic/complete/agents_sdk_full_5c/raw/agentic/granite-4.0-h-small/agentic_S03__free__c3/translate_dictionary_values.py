import os
from translation_client import get_client
from translation_models import translate_request, normalize_response

def translate_dictionary_values(data: dict, source_lang: str = 'en', target_lang: str = 'es') -> dict:
    """Translate dictionary values while preserving keys using Google Translate API.
    Non-string values are left unchanged.
    """
    client = get_client()
    translated = {}
    for k, v in data.items():
        if isinstance(v, str):
            request_data = translate_request(v, source_lang, target_lang)
            response = client.translate(request_data)
            translated[k] = normalize_response(response)
        else:
            translated[k] = v
    return translated