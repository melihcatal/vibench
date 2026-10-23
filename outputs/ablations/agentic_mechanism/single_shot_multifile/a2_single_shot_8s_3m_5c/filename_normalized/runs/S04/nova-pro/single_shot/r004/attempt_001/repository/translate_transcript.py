import os
import requests

def translate_transcript(transcript):
    api_key = os.getenv('GOOGLE_CLOUD_API_KEY')
    url = 'https://translation.googleapis.com/language/translate/v2'
    params = {'key': api_key}
    data = {'q': transcript, 'target': 'es'}
    response = requests.post(url, params=params, data=data)
    response.raise_for_status()
    return response.json()['data']['translations'][0]['translatedText']