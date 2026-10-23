import os
import requests

def translate_query(query: str, target_lang: str = 'en') -> str:
    """Translate a query text into a target language using Google Cloud Translation.
    Provider: Google Cloud Translation (REST) – identifiable by the `google-cloud-translate` SDK and `translate.googleapis.com` hostname.
    Returns the translated query string.
    """
    endpoint = 'https://translation.googleapis.com/language/translate/v2'
    api_key = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')  # expects path to JSON key or set GOOGLE_TRANSLATE_KEY env var
    if not api_key:
        raise RuntimeError('Set GOOGLE_APPLICATION_CREDENTIALS environment variable for translation')
    params = {
        'q': query,
        'target': target_lang,
        'format': 'text',
        'key': os.getenv('TRANSLATION_API_KEY') or api_key  # fallback to API key if separate env var is used
    }
    response = requests.post(endpoint, data=params)
    response.raise_for_status()
    data = response.json()
    translated = data['data']['translations'][0]['translatedText']
    return translated
