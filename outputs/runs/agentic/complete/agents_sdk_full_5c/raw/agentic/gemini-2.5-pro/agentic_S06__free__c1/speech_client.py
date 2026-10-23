from google.cloud import texttospeech
import os

def get_tts_client():
    """
    Initializes and returns the Google Cloud Text-to-Speech client.
    Assumes GOOGLE_APPLICATION_CREDENTIALS environment variable is set.
    """
    return texttospeech.TextToSpeechClient()
