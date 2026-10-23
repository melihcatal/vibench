from google.cloud import texttospeech

class SpeechClient:
    def __init__(self):
        self._client = texttospeech.TextToSpeechClient()

    def get_client(self):
        return self._client
