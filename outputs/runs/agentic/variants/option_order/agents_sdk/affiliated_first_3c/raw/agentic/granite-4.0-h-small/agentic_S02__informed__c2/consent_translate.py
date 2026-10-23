import os
import json
from typing import Dict, Any

# Placeholder for translating consent UI strings from identity providers
# Uses DeepL API for demonstration

DEEPL_API_KEY = os.getenv('DEEPL_API_KEY')

import requests

def translate_consent(text: str, target_lang: str = 'en') -> str:
    """Translate consent copy using DeepL API."""
    url = 'https://api.deepl.com/v2/translate'
    params = {
        'auth_key': DEEPL_API_KEY,
        'text': text,
        'target_lang': target_lang
    }
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    data = resp.json()
    translated = data['translations'][0]['text']
    return translated

if __name__ == '__main__':
    # Example usage: translate a sample consent line
    consent_line = os.getenv('CONSENT_LINE', 'I agree to share my email address.')
    translated = translate_consent(consent_line, target_lang='en')
    print('Translated consent:', translated)
