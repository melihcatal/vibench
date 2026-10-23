import os
from functools import lru_cache

from google.cloud import texttospeech


@lru_cache(maxsize=1)
def get_client():
    return texttospeech.TextToSpeechClient()


def get_default_voice_name():
    return os.getenv("GOOGLE_TTS_VOICE")


def get_default_language_code():
    return os.getenv("GOOGLE_TTS_LANGUAGE_CODE", "en-US")


def get_audio_encoding():
    return texttospeech.AudioEncoding.MP3
