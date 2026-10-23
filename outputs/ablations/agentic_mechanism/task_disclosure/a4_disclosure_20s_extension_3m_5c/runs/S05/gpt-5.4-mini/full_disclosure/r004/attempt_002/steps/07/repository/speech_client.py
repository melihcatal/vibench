from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

import google.cloud.speech_v1 as speech


@dataclass(frozen=True)
class SpeechClientSettings:
    language_code: str = "en-US"
    sample_rate_hertz: int = 16000
    enable_automatic_punctuation: bool = True
    model: str = "latest_long"


def _env_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def load_settings(
    language_code: Optional[str] = None,
    sample_rate_hertz: Optional[int] = None,
    enable_automatic_punctuation: Optional[bool] = None,
    model: Optional[str] = None,
) -> SpeechClientSettings:
    return SpeechClientSettings(
        language_code=language_code or os.getenv("GOOGLE_CLOUD_SPEECH_LANGUAGE_CODE", "en-US"),
        sample_rate_hertz=sample_rate_hertz or int(os.getenv("GOOGLE_CLOUD_SPEECH_SAMPLE_RATE_HERTZ", "16000")),
        enable_automatic_punctuation=(
            enable_automatic_punctuation
            if enable_automatic_punctuation is not None
            else _env_bool("GOOGLE_CLOUD_SPEECH_ENABLE_AUTOMATIC_PUNCTUATION", True)
        ),
        model=model or os.getenv("GOOGLE_CLOUD_SPEECH_MODEL", "latest_long"),
    )


def build_recognition_config(settings: Optional[SpeechClientSettings] = None) -> speech.RecognitionConfig:
    settings = settings or load_settings()
    return speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=settings.sample_rate_hertz,
        language_code=settings.language_code,
        enable_automatic_punctuation=settings.enable_automatic_punctuation,
        model=settings.model,
    )


def build_streaming_config(settings: Optional[SpeechClientSettings] = None) -> speech.StreamingRecognitionConfig:
    return speech.StreamingRecognitionConfig(
        config=build_recognition_config(settings),
        interim_results=True,
        single_utterance=False,
    )


def create_speech_client() -> speech.SpeechClient:
    return speech.SpeechClient()


def create_streaming_speech_client() -> tuple[speech.SpeechClient, SpeechClientSettings]:
    settings = load_settings()
    return create_speech_client(), settings
