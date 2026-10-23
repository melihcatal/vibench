# select_voice.py
import os
from google.cloud import texttospeech


def list_voices(language_code=None):
    """Returns a list of available voices filtered by optional language_code."""
    client = texttospeech.TextToSpeechClient()
    voices = client.list_voices(language=language_code).voices
    for v in voices:
        print(
            f"Name: {v.name}, Language: {v.language_codes[0]}, Gender: {v.ssml_gender}, Natural: {v.natural_sample_rate_hertz}"
        )


def select_voice(language_code=None):
    """Prompt user to select a voice name from the list."""
    list_voices(language_code)
    while True:
        name = input("Enter voice name: ").strip()
        for v in list_voices(language_code).voices:
            if v.name == name:
                return v.name
        print("Voice not found. Try again.")
