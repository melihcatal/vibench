import os
from google.cloud import texttospeech


def get_tts_client():
    """Initializes and returns a Google Cloud Text-to-Speech client."""
    # The GOOGLE_APPLICATION_CREDENTIALS environment variable should be set
    # to the path of your service account key file.
    return texttospeech.TextToSpeechClient()
