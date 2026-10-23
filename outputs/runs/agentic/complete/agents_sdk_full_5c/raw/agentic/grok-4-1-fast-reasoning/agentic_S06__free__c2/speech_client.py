import os
from google.cloud import texttospeech

def get_tts_client() -> texttospeech.TextToSpeechClient:
    return texttospeech.TextToSpeechClient()
