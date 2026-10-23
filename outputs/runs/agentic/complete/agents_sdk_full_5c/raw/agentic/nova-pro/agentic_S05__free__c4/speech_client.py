import os
from google.cloud import speech

def create_streaming_client():
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/credentials.json'
    return speech.SpeechClient()