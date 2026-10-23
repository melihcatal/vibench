import os
from dataclasses import dataclass
from typing import Optional

from google.cloud import speech_v1 as speech


@dataclass
class SpeechConfig:
    language_code: str = "en-US"
    enable_punctuation: bool = True
    sample_rate_hz: int = 16000
    encoding: str = "LINEAR16"


def load_speech_config() -> SpeechConfig:
    return SpeechConfig(
        language_code=os.getenv("GOOGLE_SPEECH_LANGUAGE", "en-US"),
        enable_punctuation=os.getenv("GOOGLE_SPEECH_ENABLE_PUNCTUATION", "1") != "0",
        sample_rate_hz=int(os.getenv("GOOGLE_SPEECH_SAMPLE_RATE", "16000")),
        encoding=os.getenv("GOOGLE_SPEECH_ENCODING", "LINEAR16"),
    )


def create_speech_client() -> speech.SpeechClient:
    return speech.SpeechClient()


def build_recognition_config(
    cfg: Optional[SpeechConfig] = None,
) -> speech.RecognitionConfig:
    cfg = cfg or load_speech_config()
    return speech.RecognitionConfig(
        encoding=getattr(speech.RecognitionConfig.AudioEncoding, cfg.encoding),
        language_code=cfg.language_code,
        enable_automatic_punctuation=cfg.enable_punctuation,
        sample_rate_hertz=cfg.sample_rate_hz,
    )
