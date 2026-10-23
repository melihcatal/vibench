import os
from dataclasses import dataclass
from typing import Optional

from google.cloud import speech_v1p1beta1 as speech


@dataclass
class SpeechConfig:
    language_code: str = os.getenv("GOOGLE_SPEECH_LANGUAGE_CODE", "en-US")
    enable_punctuation: bool = os.getenv("GOOGLE_SPEECH_ENABLE_PUNCTUATION", "true").lower() == "true"
    sample_rate_hertz: int = int(os.getenv("GOOGLE_SPEECH_SAMPLE_RATE_HERTZ", "16000"))
    encoding: str = os.getenv("GOOGLE_SPEECH_ENCODING", "LINEAR16")


def create_speech_client() -> speech.SpeechClient:
    return speech.SpeechClient()


def create_recognition_config(config: Optional[SpeechConfig] = None) -> speech.RecognitionConfig:
    cfg = config or SpeechConfig()
    return speech.RecognitionConfig(
        encoding=getattr(speech.RecognitionConfig.AudioEncoding, cfg.encoding),
        sample_rate_hertz=cfg.sample_rate_hertz,
        language_code=cfg.language_code,
        enable_automatic_punctuation=cfg.enable_punctuation,
    )


def create_streaming_config(config: Optional[SpeechConfig] = None) -> speech.StreamingRecognitionConfig:
    return speech.StreamingRecognitionConfig(
        config=create_recognition_config(config),
        interim_results=True,
        single_utterance=False,
    )
