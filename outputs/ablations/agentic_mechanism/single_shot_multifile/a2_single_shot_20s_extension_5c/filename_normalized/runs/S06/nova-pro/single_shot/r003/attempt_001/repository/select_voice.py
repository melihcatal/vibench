import os
from google.cloud import texttospeech

client = texttospeech.TextToSpeechClient()

def select_voice(language_code):
    voices = client.list_voices(language_code=language_code).voices
    return voices