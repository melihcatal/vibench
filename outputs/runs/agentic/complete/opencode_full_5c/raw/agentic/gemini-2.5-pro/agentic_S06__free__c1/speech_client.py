import os
from google.cloud import texttospeech


def get_speech_client():
    """Initializes and returns a Google Cloud TextToSpeechClient."""
    # Instantiates a client. Expects GOOGLE_APPLICATION_CREDENTIALS to be set.
    return texttospeech.TextToSpeechClient()
