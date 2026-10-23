from speech_client import get_text_to_speech_client
from google.cloud import texttospeech


def list_voices(language_code=None):
    client = get_text_to_speech_client()
    voices = client.list_voices(language_code=language_code).voices
    return voices


def select_voice_by_locale(language_code, gender=None, name=None):
    voices = list_voices(language_code=language_code)
    for voice in voices:
        if name and voice.name == name:
            return voice
        if gender and voice.ssml_gender == gender:
            return voice
    return None
