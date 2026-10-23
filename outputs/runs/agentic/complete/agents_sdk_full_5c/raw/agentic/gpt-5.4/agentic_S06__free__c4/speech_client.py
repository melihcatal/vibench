from __future__ import annotations

import os
from typing import Optional

from google.cloud import texttospeech


DEFAULT_TTS_MODEL_FAMILY = "Google Cloud Text-to-Speech"


def get_google_tts_client(credentials_path: Optional[str] = None) -> texttospeech.TextToSpeechClient:
    if credentials_path:
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
    return texttospeech.TextToSpeechClient()


def get_project_hint() -> Optional[str]:
    return os.getenv("GOOGLE_CLOUD_PROJECT")


def default_audio_encoding() -> texttospeech.AudioEncoding:
    return texttospeech.AudioEncoding.MP3


def resolve_audio_encoding(name: str) -> texttospeech.AudioEncoding:
    normalized = (name or "MP3").upper()
    if not hasattr(texttospeech.AudioEncoding, normalized):
        raise ValueError(f"Unsupported Google Cloud TTS audio encoding: {name}")
    return getattr(texttospeech.AudioEncoding, normalized)
