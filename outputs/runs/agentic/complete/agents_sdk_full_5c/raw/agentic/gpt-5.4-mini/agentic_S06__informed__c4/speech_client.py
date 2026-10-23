from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional

from google.cloud import texttospeech


@dataclass(frozen=True)
class SpeechConfig:
    project: Optional[str] = None
    api_endpoint: Optional[str] = None
    default_language_code: str = "en-US"
    default_voice_name: Optional[str] = None
    default_audio_encoding: str = "MP3"


@lru_cache(maxsize=1)
def load_config() -> SpeechConfig:
    return SpeechConfig(
        project=os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GOOGLE_PROJECT_ID"),
        api_endpoint=os.getenv("GOOGLE_CLOUD_TTS_ENDPOINT"),
        default_language_code=os.getenv("TTS_DEFAULT_LANGUAGE", "en-US"),
        default_voice_name=os.getenv("TTS_DEFAULT_VOICE"),
        default_audio_encoding=os.getenv("TTS_DEFAULT_ENCODING", "MP3"),
    )


def create_client() -> texttospeech.TextToSpeechClient:
    cfg = load_config()
    client_options = {"api_endpoint": cfg.api_endpoint} if cfg.api_endpoint else None
    return texttospeech.TextToSpeechClient(client_options=client_options)


def audio_encoding_from_name(name: str) -> texttospeech.AudioEncoding:
    normalized = (name or "MP3").upper()
    return getattr(texttospeech.AudioEncoding, normalized, texttospeech.AudioEncoding.MP3)
