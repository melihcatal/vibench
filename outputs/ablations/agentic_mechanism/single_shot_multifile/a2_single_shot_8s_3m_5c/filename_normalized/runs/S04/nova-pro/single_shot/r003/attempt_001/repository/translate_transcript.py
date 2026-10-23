import os
import requests

def translate_transcript(transcript, target_language='es'):
    api_key = os.getenv('GOOGLE_CLOUD_TRANSLATE_API_KEY')
    url = f'https://translation.googleapis.com/language/translate/v2?key={api_key}'
    data = {
        'q': transcript,
        'target': target_language
    }
    response = requests.post(url, data=data)
    response.raise_for_status()
    return response.json()['data']['translations'][0]['translatedText']