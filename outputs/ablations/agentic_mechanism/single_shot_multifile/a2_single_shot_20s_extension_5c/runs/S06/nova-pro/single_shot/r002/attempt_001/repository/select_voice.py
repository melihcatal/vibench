import os
from google.cloud import texttospeech

def select_voice(language_code):
    client = texttospeech.TextToSpeechClient()
    response = client.list_voices(language_code=language_code)
    return [(voice.name, voice.ssml_gender.name) for voice in response.voices]