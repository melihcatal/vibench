import os
import requests

def translate_transcript(transcript):
    api_key = os.getenv('GOOGLE_CLOUD_TRANSLATE_API_KEY')
    url = 'https://translation.googleapis.com/language/translate/v2'
    params = {
        'q': transcript,
        'target': 'es',
        'format': 'text',
        'key': api_key
    }
    response = requests.get(url, params=params)
    return response.json()['data']['translations'][0]['translatedText']