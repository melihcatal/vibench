from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

from google.cloud import speech


@dataclass(frozen=True)
class SpeechConfig:
    project_id: Optional[str] = None
    location: str = os.getenv("GOOGLE_CLOUD_LOCATION", "global")
    model: str = os.getenv("GOOGLE_CLOUD_SPEECH_MODEL", "latest_long")
    language_code: str = os.getenv("GOOGLE_CLOUD_SPEECH_LANGUAGE", "en-US")
    punctuation: bool = os.getenv("GOOGLE_CLOUD_SPEECH_PUNCTUATION", "true").lower() == "true"


def load_config() -> SpeechConfig:
    return SpeechConfig(project_id=os.getenv("GOOGLE_CLOUD_PROJECT"))


def create_speech_client() -> speech.SpeechClient:
    return speech.SpeechClient()


def stream_recognition_config(cfg: Optional[SpeechConfig] = None) -> speech.RecognitionConfig:
    cfg = cfg or load_config()
    return speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code=cfg.language_code,
        enable_automatic_punctuation=cfg.punctuation,
        model=cfg.model,
        audio_channel_count=1,
    )


def streaming_config(cfg: Optional[SpeechConfig] = None) -> speech.StreamingRecognitionConfig:
    return speech.StreamingRecognitionConfig(
        config=stream_recognition_config(cfg),
        interim_results=True,
        single_utterance=False,
    )
