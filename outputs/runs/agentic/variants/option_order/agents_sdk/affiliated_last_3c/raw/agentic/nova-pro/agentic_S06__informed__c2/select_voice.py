import os
from google.cloud import texttospeech

def list_voices():
    client = texttospeech.TextToSpeechClient()
    voices = client.list_voices()
    return [voice.name for voice in voices]