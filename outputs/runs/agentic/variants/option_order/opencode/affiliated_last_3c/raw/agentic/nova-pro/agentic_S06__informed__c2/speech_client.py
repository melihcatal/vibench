import os
from google.cloud import texttospeech


def get_speech_client():
    return texttospeech.TextToSpeechClient()
