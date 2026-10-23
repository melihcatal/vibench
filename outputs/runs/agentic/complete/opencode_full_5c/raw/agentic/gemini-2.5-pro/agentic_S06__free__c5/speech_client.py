import os
from google.cloud import texttospeech


def get_speech_client():
    """Initializes and returns a Google Cloud Text-to-Speech client."""
    # The client uses Application Default Credentials to authenticate.
    # For more details, see:
    # https://cloud.google.com/docs/authentication/production
    return texttospeech.TextToSpeechClient()
