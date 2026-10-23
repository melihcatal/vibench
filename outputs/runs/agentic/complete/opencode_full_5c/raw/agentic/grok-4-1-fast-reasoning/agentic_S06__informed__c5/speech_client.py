import os
from google.cloud import texttospeech
from google.cloud import storage


def get_tts_client():
    return texttospeech.TextToSpeechClient()


def get_storage_client():
    return storage.Client()
