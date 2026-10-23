import os
from google.cloud import texttospeech


def get_speech_client():
    """Initializes and returns a Google Cloud Text-to-Speech client."""
    # The client uses GOOGLE_APPLICATION_CREDENTIALS environment variable for auth
    return texttospeech.TextToSpeechClient()
