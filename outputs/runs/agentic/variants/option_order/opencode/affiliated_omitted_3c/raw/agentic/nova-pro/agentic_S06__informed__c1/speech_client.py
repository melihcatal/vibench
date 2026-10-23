import os
from google.cloud import texttospeech


def get_speech_client():
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/credentials.json"
    return texttospeech.TextToSpeechClient()
