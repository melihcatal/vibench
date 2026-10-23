import os
import requests


def translate_text(text, locale):
    api_key = os.getenv('GOOGLE_TRANSLATE_API_KEY')
    url = f'https://translation.googleapis.com/language/translate/v2?key={api_key}'
    response = requests.post(url, data={"q": text, "target": locale})
    return response.json()['data']['translations'][0]['translatedText']
