import os
from google.cloud import texttospeech

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/credentials.json'

client = texttospeech.TextToSpeechClient()

def list_voices():
    voices = client.list_voices()
    for voice in voices.voices:
        print(f'Name: {voice.name}, Language Code: {voice.language_codes[0]}')