import os
from google.cloud import texttospeech

def get_tts_client():
    """
    Provides Google Cloud Text-to-Speech client helper.
    Assumes GOOGLE_APPLICATION_CREDENTIALS is set.
    """
    return texttospeech.TextToSpeechClient()