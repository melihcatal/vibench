from google.cloud import texttospeech_v1 as texttospeech
import os


def list_voices(language_code: str = None):
    client = texttospeech.TextToSpeechClient()
    voices = client.list_voices(language_code=language_code).voices
    return [
        {
            "name": voice.name,
            "language_codes": voice.language_codes,
            "gender": voice.ssml_gender,
        }
        for voice in voices
    ]


def select_voice_by_locale(language_code: str, preferred_gender: str = None):
    available_voices = list_voices(language_code=language_code)
    if preferred_gender:
        for voice in available_voices:
            if voice["gender"].name == preferred_gender.upper():
                return voice
    if available_voices:
        return available_voices[0]
    return None
