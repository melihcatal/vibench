import os
from google.cloud import texttospeech

def get_text_to_speech_client() -> texttospeech.TextToSpeechClient:
    """
    Initializes and returns a Google Cloud Text-to-Speech client.
    Uses GOOGLE_APPLICATION_CREDENTIALS for authentication.
    """
    # Google Cloud Text-to-Speech client
    return texttospeech.TextToSpeechClient()
