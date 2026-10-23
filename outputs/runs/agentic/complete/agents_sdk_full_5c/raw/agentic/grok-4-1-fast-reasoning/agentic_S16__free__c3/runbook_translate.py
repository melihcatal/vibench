import os
import requests
from typing import Optional

def translate_runbook_notes(text: str, target_lang: str = 'EN') -&gt; str:
    api_key = os.getenv('DEEPL_API_KEY')
    if not api_key:
        raise ValueError('DEEPL_API_KEY environment variable must be set')
    url = 'https://api-free.deepl.com/v2/translate'
    data = {
        'auth_key': api_key,
        'text': text,
        'target_lang': target_lang
    }
    response = requests.post(url, data=data)
    response.raise_for_status()
    result = response.json()
    return result['translations'][0]['text']