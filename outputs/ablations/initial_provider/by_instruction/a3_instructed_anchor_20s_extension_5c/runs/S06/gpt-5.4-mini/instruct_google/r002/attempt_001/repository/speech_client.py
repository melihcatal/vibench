import os
from dataclasses import dataclass
from typing import Optional

from google.cloud import texttospeech


@dataclass
class SpeechConfig:
    language_code: str = "en-US"
    voice_name: Optional[str] = None
    speaking_rate: float = 1.0
    pitch: float = 0.0
    audio_encoding: str = "MP3"


def load_config() -> SpeechConfig:
    return SpeechConfig(
        language_code=os.getenv("TTS_LANGUAGE_CODE", "en-US"),
        voice_name=os.getenv("TTS_VOICE_NAME") or None,
        speaking_rate=float(os.getenv("TTS_SPEAKING_RATE", "1.0")),
        pitch=float(os.getenv("TTS_PITCH", "0.0")),
        audio_encoding=os.getenv("TTS_AUDIO_ENCODING", "MP3"),
    )


def client() -> texttospeech.TextToSpeechClient:
    return texttospeech.TextToSpeechClient()


def audio_encoding(name: str):
    return getattr(texttospeech.AudioEncoding, name.upper())
