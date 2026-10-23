import os
from google.cloud import texttospeech


def get_tts_client():
    """Returns a Google Cloud Text-to-Speech client."""
    # GOOGLE_APPLICATION_CREDENTIALS environment variable is expected for authentication
    return texttospeech.TextToSpeechClient()
