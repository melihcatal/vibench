import os
from google.cloud import speech_v1p1beta1 as speech

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/credentials.json'

client = speech.SpeechClient()

class SpeechClient:
    def __init__(self):
        self.client = client

    def get_client(self):
        return self.client
