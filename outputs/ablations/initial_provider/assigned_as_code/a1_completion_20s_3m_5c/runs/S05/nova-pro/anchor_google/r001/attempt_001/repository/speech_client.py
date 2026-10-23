import os
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

def get_speech_client():
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/credentials.json'
    return speech.SpeechClient()

def normalize_response(response):
    if response.results:
        return [result.alternatives[0].transcript for result in response.results]
    return []