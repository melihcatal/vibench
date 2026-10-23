import os
from translation_client import get_client
from translation_models import translate_request, normalize_response

def translate_text(source_text: str, source_lang: str = 'en', target_lang: str = 'es') -> str:
    """Translate a single text string between languages using Google Translate API.
    """
    client = get_client()
    request_data = translate_request(source_text, source_lang, target_lang)
    response = client.translate(request_data)
    return normalize_response(response)