import os
from google.cloud import texttospeech


def get_tts_client():
    """
    Returns a Google Cloud Text-to-Speech client.
    Requires GOOGLE_APPLICATION_CREDENTIALS to be set.
    """
    return texttospeech.TextToSpeechClient()
