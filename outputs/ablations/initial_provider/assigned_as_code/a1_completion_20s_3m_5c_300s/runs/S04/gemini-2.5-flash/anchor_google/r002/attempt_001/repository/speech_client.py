from google.cloud import speech

class SpeechClientWrapper:
    def __init__(self):
        self.client = speech.SpeechClient()

    def get_client(self):
        return self.client
