import os
import requests
from database_models import normalize_item

def translate_document(document_id: str, raw_item: dict, target_lang: str = 'es') -> dict:
    """Translate user‑facing fields of a DynamoDB document using Google Cloud Translation.
    Returns a new dict with translated values.
    """
    item = normalize_item(raw_item)
    # Fields to translate (configurable)
    fields = ['title', 'content', 'description']
    translated = {}
    for f in fields:
        text = str(item.get(f, ''))
        if not text:
            continue
        endpoint = 'https://translation.googleapis.com/language/translate/v2'
        api_key = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')  # using env credential file
        params = {
            'q': text,
            'target': target_lang,
            'format': 'text',
            'key': os.getenv('TRANSLATION_API_KEY')
        }
        r = requests.post(endpoint, params=params, json=None, timeout=5)
        if r.status_code != 200:
            raise RuntimeError(f'Translation API error: {r.status_code}')
        data = r.json()
        translated[f] = data['data']['translations'][0]['translatedText']
    # Preserve original non‑translated fields
    for k, v in item.items():
        if k not in translated:
            translated[k] = v
    return translated
