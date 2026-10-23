import os
from typing import Optional

from google.cloud import texttospeech


def _get_credentials_path() -> Optional[str]:
    return os.getenv("GOOGLE_APPLICATION_CREDENTIALS")


def build_client() -> texttospeech.TextToSpeechClient:
    return texttospeech.TextToSpeechClient()


def default_voice_language() -> str:
    return os.getenv("TTS_DEFAULT_LOCALE", "en-US")


def default_voice_name() -> Optional[str]:
    return os.getenv("TTS_DEFAULT_VOICE")


def default_audio_encoding() -> texttospeech.AudioEncoding:
    return texttospeech.AudioEncoding.MP3
