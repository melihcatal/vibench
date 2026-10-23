import os
import requests

def generate_audio_preview(text, language_code):
    response = requests.post(
        'https://texttospeech.googleapis.com/v1/text:synthesize?key=' + os.getenv('GOOGLE_CLOUD_TEXT_TO_SPEECH_API_KEY'),
        json={
            'input': {'text': text},
            'voice': {'languageCode': language_code,'ssmlGender': 'NEUTRAL'},
            'audioConfig': {'audioEncoding': 'MP3'}
        }
    )
    return response.json()['audioContent']