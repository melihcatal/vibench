import os
from google.cloud import speech_v1p1beta1 as speech

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/your/credentials.json'

def get_speech_client():
    return speech.SpeechClient()