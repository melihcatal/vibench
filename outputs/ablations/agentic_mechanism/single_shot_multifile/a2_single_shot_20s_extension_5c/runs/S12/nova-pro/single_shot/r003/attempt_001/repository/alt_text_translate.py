import os
import requests

TRANSLATE_API_KEY = os.getenv('TRANSLATE_API_KEY')

def translate_text(text, target_language='es'):
    response = requests.post(
        'https://translation.googleapis.com/language/translate/v2',
        params={'key': TRANSLATE_API_KEY},
        data={'q': text, 'target': target_language}
    )
    return response.json()['data']['translations'][0]['translatedText']