import os
from speech_client import TextToSpeechClient

def list_voices(locale=None):
    client = TextToSpeechClient()
    voices = client.list_voices(language_code=locale)
    for v in voices:
        print(f"ID: {v.name}, Language: {v.language_codes[0] if v.language_codes else 'N/A'}, Gender: {v.ssml_gender}, Name: {v.name}")
    return voices

def select_voice(locale):
    voices = list_voices(locale)
    if not voices:
        return None
    # Simple interactive selection (remove in production)
    idx = int(input("Enter voice index: "))
    return voices[idx].name
