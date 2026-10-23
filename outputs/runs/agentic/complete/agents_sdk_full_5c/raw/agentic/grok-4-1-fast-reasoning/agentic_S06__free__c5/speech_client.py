import os
from google.cloud import texttospeech

def get_tts_client():
    """
    Returns a configured Google Cloud Text-to-Speech client.
    Assumes GOOGLE_APPLICATION_CREDENTIALS environment variable is set.
    """
    return texttospeech.TextToSpeechClient()
