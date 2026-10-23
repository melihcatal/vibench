from google.cloud import texttospeech_v1 as texttospeech
import os
from typing import Optional


class SpeechClient:
    def __init__(self):
        self.client = texttospeech.TextToSpeechClient()

    def get_client(self):
        return self.client

    @staticmethod
    def load_config():
        return {"credentials": os.getenv("GOOGLE_APPLICATION_CREDENTIALS")}
