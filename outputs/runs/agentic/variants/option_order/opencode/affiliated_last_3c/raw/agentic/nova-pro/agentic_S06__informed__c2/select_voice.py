import os
from google.cloud import texttospeech


def select_voice():
    client = texttospeech.TextToSpeechClient()
    voices = client.list_voices()
    return [voice for voice in voices]
