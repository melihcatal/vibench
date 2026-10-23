import os
import google.cloud.speech


class SpeechClient:
    def __init__(self):
        # GOOGLE_APPLICATION_CREDENTIALS environment variable is expected to be set
        self.client = google.cloud.speech.SpeechClient()

    def get_client(self):
        return self.client
