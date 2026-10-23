import os
import requests

TRANSLATE_API_KEY = os.getenv('TRANSLATE_API_KEY')

def translate_text(text, target_language='es'):
    url = 'https://translation.googleapis.com/language/translate/v2'
    params = {
        'q': text,
        'target': target_language,
        'key': TRANSLATE_API_KEY
    }
    response = requests.get(url, params=params)
    return response.json()['data']['translations'][0]['translatedText']