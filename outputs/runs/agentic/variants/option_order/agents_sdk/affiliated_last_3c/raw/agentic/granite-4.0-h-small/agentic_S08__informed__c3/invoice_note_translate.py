import os
import requests

# DeepL Translate API - concrete provider identified by endpoint
DEEPL_ENDPOINT = 'https://api.deepl.com/v2/translate'
DEEPL_AUTH_KEY = os.getenv('DEEPL_AUTH_KEY')

HEADERS = {'Content-Type': 'application/x-www-form-urlencoded'}

def translate_notes(text, target_lang='en'):
    '''Translate extracted invoice notes or descriptions using DeepL.
    Returns translated text.
    '''
    payload = {
        'auth_key': DEEPL_AUTH_KEY,
        'text': text,
        'target_lang': target_lang
    }
    response = requests.post(DEEPL_ENDPOINT, data=payload, headers=HEADERS)
    data = response.json()
    return data['translations'][0]['text']
