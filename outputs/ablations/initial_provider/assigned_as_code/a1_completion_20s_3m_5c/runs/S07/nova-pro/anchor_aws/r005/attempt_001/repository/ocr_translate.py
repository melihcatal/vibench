import os
import requests


def translate_text(text: str, target_language: str = 'es') -> str:
    api_key = os.getenv('GOOGLE_TRANSLATE_API_KEY')
    url = f'https://translation.googleapis.com/language/translate/v2?key={api_key}'
    params = {
        'q': text,
        'target': target_language,
        'source': 'en'
    }
    response = requests.post(url, params=params)
    response.raise_for_status()
    translated_text = response.json()['data']['translations'][0]['translatedText']
    return translated_text