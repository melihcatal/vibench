import os
from dataclasses import dataclass
from typing import Optional

from google.cloud import speech


@dataclass
class SpeechConfig:
    language_code: str = os.getenv("GOOGLE_SPEECH_LANGUAGE_CODE", "en-US")
    sample_rate_hz: int = int(os.getenv("GOOGLE_SPEECH_SAMPLE_RATE_HZ", "16000"))
    enable_punctuation: bool = os.getenv("GOOGLE_SPEECH_ENABLE_PUNCTUATION", "1") == "1"


def build_speech_client() -> speech.SpeechClient:
    return speech.SpeechClient()


def streaming_config(language_code: Optional[str] = None, enable_punctuation: Optional[bool] = None, sample_rate_hz: Optional[int] = None) -> speech.StreamingRecognitionConfig:
    cfg = SpeechConfig()
    recognition_config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=sample_rate_hz or cfg.sample_rate_hz,
        language_code=language_code or cfg.language_code,
        enable_automatic_punctuation=cfg.enable_punctuation if enable_punctuation is None else enable_punctuation,
    )
    return speech.StreamingRecognitionConfig(
        config=recognition_config,
        interim_results=True,
        single_utterance=False,
    )
