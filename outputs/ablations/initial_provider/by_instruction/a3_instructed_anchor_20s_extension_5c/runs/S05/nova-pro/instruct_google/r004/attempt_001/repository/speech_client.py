import os
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

def create_speech_client():
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/credentials.json'
    client = speech.SpeechClient()
    return client