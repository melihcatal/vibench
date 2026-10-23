import os
import math
import requests
from typing import List

# DeepL REST API endpoint (no SDK needed)
DEEPL_AUTH_KEY = os.getenv('DEEPL_AUTH_KEY')
if not DEEPL_AUTH_KEY:
    raise RuntimeError('Set DEEPL_AUTH_KEY environment variable')

DEEPL_ENDPOINT = 'https://api.deepl.com/v2/translate'


def translate_query(query: str, target_lang: str = 'en') -> str:
    """Translate a text query using DeepL API.

    Returns the translated query.
    """
    params = {
        'auth_key': DEEPL_AUTH_KEY,
        'text': query,
        'target_lang': target_lang,
    }
    resp = requests.post(DEEPL_ENDPOINT, data=params)
    resp.raise_for_status()
    data = resp.json()
    # DeepL returns translated_text inside 'translations'[0]['text']
    translated = data['translations'][0]['text']
    return translated
