from google.cloud import texttospeech

from speech_client import get_tts_client


def select_voice(locale: str):
    client = get_tts_client()
    voices = client.list_voices(language_code=locale).voices
    return [voice.name for voice in voices]
