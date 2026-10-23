import os
from google.cloud import texttospeech


def load_config(config=None):
    base = dict(config or {})
    if "language_code" not in base:
        base["language_code"] = os.getenv("TTS_LANGUAGE_CODE", "en-US")
    if "audio_encoding" not in base:
        base["audio_encoding"] = texttospeech.AudioEncoding.MP3
    return base


def client():
    return texttospeech.TextToSpeechClient()


def audio_encoding_name(encoding):
    return texttospeech.AudioEncoding.Name(encoding)
