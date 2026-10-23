import requests
import os

DEEPL_URL = "https://api-free.deepl.com/v2/translate"
DEEPL_AUTH_KEY = os.getenv('DEEPL_AUTH_KEY')

def translate_log_message(text: str, target_lang: str = 'FR') -> str:
    if not DEEPL_AUTH_KEY:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set")
    response = requests.post(DEEPL_URL, data={
        'auth_key': DEEPL_AUTH_KEY,
        'text': text,
        'target_lang': target_lang.upper()
    })
    response.raise_for_status()
    result = response.json()
    return result['translations'][0]['text']
