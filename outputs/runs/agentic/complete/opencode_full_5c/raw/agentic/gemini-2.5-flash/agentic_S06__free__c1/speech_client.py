from google.cloud import texttospeech_v1 as texttospeech
import os


def get_tts_client():
    return texttospeech.TextToSpeechClient()
