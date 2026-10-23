from google.cloud import texttospeech
from speech_client import get_client

def select_voice(language_code):
    client = get_client()
    voices = client.list_voices(language_codes_filter=[language_code])
    return [voice.name for voice in voices]