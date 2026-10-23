from google.cloud.speech import enums
from google.cloud.speech import types

class TranscriptionRequest:
    def __init__(self, audio, config):
        self.audio = audio
        self.config = config

class TranscriptionResponse:
    def __init__(self, response):
        self.response = response