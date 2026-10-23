import os
from google.cloud import texttospeech


def get_text_to_speech_client():
    """Initializes and returns a Google Cloud Text-to-Speech client."""
    # GOOGLE_APPLICATION_CREDENTIALS environment variable should be set
    return texttospeech.TextToSpeechClient()
