from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional

from google.cloud import texttospeech


@dataclass(frozen=True)
class TTSConfig:
    voice_name: Optional[str] = None
    language_code: str = "en-US"
    speaking_rate: float = 1.0
    pitch: float = 0.0
    audio_encoding: str = "MP3"


@lru_cache(maxsize=1)
def get_tts_client() -> texttospeech.TextToSpeechClient:
    return texttospeech.TextToSpeechClient()


@lru_cache(maxsize=1)
def get_config() -> TTSConfig:
    return TTSConfig(
        voice_name=os.getenv("TTS_VOICE_NAME") or None,
        language_code=os.getenv("TTS_LANGUAGE_CODE", "en-US"),
        speaking_rate=float(os.getenv("TTS_SPEAKING_RATE", "1.0")),
        pitch=float(os.getenv("TTS_PITCH", "0.0")),
        audio_encoding=os.getenv("TTS_AUDIO_ENCODING", "MP3").upper(),
    )
