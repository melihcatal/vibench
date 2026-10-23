import os
import requests

DEEPL_AUTH_KEY = os.getenv('DEEPL_AUTH_KEY')

def translate_identity_consent_copy(text: str, target_lang: str = 'EN', source_lang: str = 'auto') -> str:
    url = 'https://api-free.deepl.com/v2/translate'
    data = {
        'auth_key': DEEPL_AUTH_KEY,
        'text': text,
        'target_lang': target_lang,
        'source_lang': source_lang,
    }
    response = requests.post(url, data=data)
    response.raise_for_status()
    translations = response.json()['translations']
    return translations[0]['text']
