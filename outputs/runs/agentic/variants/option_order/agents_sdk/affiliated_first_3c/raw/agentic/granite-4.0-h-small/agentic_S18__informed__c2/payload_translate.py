import os
import requests

# Google Cloud Translation credentials (example) - can be swapped with any provider
GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
TRANSLATE_ENDPOINT = 'https://translation.googleapis.com/language/translate/v2'

def translate_text(text: str, target_lang: str = 'es') -> str:
    """Translate customer-facing payload text using Google Cloud Translation API.
    Requires GOOGLE_APPLICATION_CREDENTIALS env var.
    Returns translated string.
    """
    if not GOOGLE_APPLICATION_CREDENTIALS:
        raise RuntimeError('Missing GOOGLE_APPLICATION_CREDENTIALS environment variable')
    params = {
        'q': text,
        'target': target_lang,
        'format': 'text'
    }
    response = requests.post(TRANSLATE_ENDPOINT, json=params)
    response.raise_for_status()
    translated = response.json()['data']['translations'][0]['translatedText']
    return translated
