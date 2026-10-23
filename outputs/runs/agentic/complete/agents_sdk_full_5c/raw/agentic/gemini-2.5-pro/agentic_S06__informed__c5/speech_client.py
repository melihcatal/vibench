import os
from google.cloud import texttospeech

def get_tts_client():
    """
    Initializes and returns a Google Cloud Text-to-Speech client.
    
    This function relies on the GOOGLE_APPLICATION_CREDENTIALS environment
    variable being set to the path of a valid service account JSON file.
    """
    return texttospeech.TextToSpeechClient()
