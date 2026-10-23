import os
from translation_client import build_client
from translation_models import normalize_request, normalize_response

PROVIDER_NAME = os.getenv('PROVIDER_NAME', 'google_translate')  # default

def translate_text(user_text, source_lang='en', target_lang='es'):
    """Translate a single text string.",
    client = build_client()
    request_payload = normalize_request(user_text, source_lang, target_lang)
    response = client.translate_text([request_payload])  # adapter-specific
    normalized = normalize_response(response[0], source_lang, target_lang)
    return normalized['translated_text']