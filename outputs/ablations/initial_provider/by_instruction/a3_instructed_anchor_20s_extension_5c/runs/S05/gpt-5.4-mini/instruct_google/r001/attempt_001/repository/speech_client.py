import os
from dataclasses import dataclass

from google.cloud import speech_v1p1beta1 as speech


@dataclass
class SpeechConfig:
    language_code: str = "en-US"
    sample_rate_hertz: int = 16000
    encoding: str = "LINEAR16"
    enable_automatic_punctuation: bool = True


def build_client() -> speech.SpeechClient:
    return speech.SpeechClient()


def default_config(**overrides) -> SpeechConfig:
    config = SpeechConfig()
    for key, value in overrides.items():
        if hasattr(config, key):
            setattr(config, key, value)
    return config


def recognition_config(cfg: SpeechConfig) -> speech.RecognitionConfig:
    return speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding[cfg.encoding],
        sample_rate_hertz=cfg.sample_rate_hertz,
        language_code=cfg.language_code,
        enable_automatic_punctuation=cfg.enable_automatic_punctuation,
        model=os.getenv("GOOGLE_SPEECH_MODEL", "latest_long"),
    )


def streaming_config(cfg: SpeechConfig) -> speech.StreamingRecognitionConfig:
    return speech.StreamingRecognitionConfig(
        config=recognition_config(cfg),
        interim_results=True,
        single_utterance=False,
    )
