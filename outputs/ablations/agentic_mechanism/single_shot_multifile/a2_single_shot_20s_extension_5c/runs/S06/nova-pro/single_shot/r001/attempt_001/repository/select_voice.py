import os
from google.cloud import texttospeech

client = texttospeech.TextToSpeechClient()

def list_voices(language_code):
    voices = client.list_voices(language_codes=[language_code]).voices
    return voices