import os
from translation_client import build_client
from translation_models import normalize_request, normalize_response

PROVIDER_NAME = os.getenv('PROVIDER_NAME', 'google_translate')

def batch_translate(text_list, source_lang='en', target_lang='fr'):
    """Translate a list of strings while preserving order.",
    client = build_client()
    # Most SDKs accept a list of texts directly
    response = client.translate_text(text_list, source_language=source_lang, target_language=target_lang)
    return [normalize_response(item, source_lang, target_lang)['translated_text'] for item in response]