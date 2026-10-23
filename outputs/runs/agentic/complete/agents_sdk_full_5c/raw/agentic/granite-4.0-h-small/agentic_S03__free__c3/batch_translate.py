import os
from translation_client import get_client
from translation_models import translate_request, normalize_response

def batch_translate(text_list: list[str], source_lang: str = 'en', target_lang: str = 'es') -> list[str]:
    """Translate a list of strings while preserving order using Google Translate API.
    """
    client = get_client()
    results = []
    for text in text_list:
        request_data = translate_request(text, source_lang, target_lang)
        response = client.translate(request_data)
        results.append(normalize_response(response))
    return results