import os
from translation_client import build_client
from translation_models import normalize_request, normalize_response

PROVIDER_NAME = os.getenv('PROVIDER_NAME', 'google_translate')

def translate_markup(html_string, source_lang='en', target_lang='de'):
    """Translate HTML/markup while preserving tags.",
    client = build_client()
    # Pass the raw markup; provider handles placeholders
    response = client.translate_text(
        [{'text': html_string, 'source_language': source_lang, 'target_language': target_lang}]
    )
    return normalize_response(response[0], source_lang, target_lang)['translated_text']