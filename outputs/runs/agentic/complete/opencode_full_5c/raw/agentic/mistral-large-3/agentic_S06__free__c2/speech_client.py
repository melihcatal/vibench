from google.cloud import texttospeech_v1 as tts
import os


class SpeechClient:
    def __init__(self):
        self.client = tts.TextToSpeechClient()
        self.credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        if not self.credentials_path:
            raise ValueError(
                "GOOGLE_APPLICATION_CREDENTIALS environment variable not set"
            )

    def get_client(self):
        return self.client
