from google.cloud import texttospeech_v1 as tts
import os
from typing import Optional


class SpeechClient:
    def __init__(self, credentials_path: Optional[str] = None):
        if credentials_path:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
        self.client = tts.TextToSpeechClient()

    def get_client(self):
        return self.client

    def set_voice(self, voice_name: str):
        self.voice_name = voice_name

    def get_default_voice(self, language_code: str = "en-US"):
        response = self.client.list_voices(language_code=language_code)
        return response.voices[0].name
