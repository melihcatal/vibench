from google.cloud import texttospeech

class TextToSpeechClientHelper:
    def __init__(self):
        self.client = texttospeech.TextToSpeechClient()

    def get_client(self):
        return self.client
