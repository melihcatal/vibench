import os
from typing import List, Optional

from google.cloud import texttospeech


def get_client() -> texttospeech.TextToSpeechClient:
    return texttospeech.TextToSpeechClient()


def default_voice_name() -> Optional[str]:
    return os.getenv("GCP_TTS_VOICE_NAME")


def default_language_code() -> Optional[str]:
    return os.getenv("GCP_TTS_LANGUAGE_CODE")


def default_audio_encoding() -> str:
    return os.getenv("GCP_TTS_AUDIO_ENCODING", "MP3")


def list_voices(language_code: Optional[str] = None):
    client = get_client()
    response = client.list_voices(
        language_code=language_code or default_language_code() or ""
    )
    return response.voices
