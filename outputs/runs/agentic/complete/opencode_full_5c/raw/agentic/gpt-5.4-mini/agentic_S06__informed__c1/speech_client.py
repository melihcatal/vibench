import os
from dataclasses import dataclass
from typing import Optional

from google.cloud import texttospeech


@dataclass
class SpeechConfig:
    language_code: str = os.getenv("TTS_LANGUAGE_CODE", "en-US")
    voice_name: Optional[str] = os.getenv("TTS_VOICE_NAME")
    speaking_rate: float = float(os.getenv("TTS_SPEAKING_RATE", "1.0"))
    pitch: float = float(os.getenv("TTS_PITCH", "0.0"))
    audio_encoding: str = os.getenv("TTS_AUDIO_ENCODING", "MP3")


def get_client() -> texttospeech.TextToSpeechClient:
    return texttospeech.TextToSpeechClient()


def audio_encoding_value(name: str):
    return getattr(texttospeech.AudioEncoding, name.upper())


def voice_params(cfg: SpeechConfig) -> texttospeech.VoiceSelectionParams:
    params = {"language_code": cfg.language_code}
    if cfg.voice_name:
        params["name"] = cfg.voice_name
    return texttospeech.VoiceSelectionParams(**params)
