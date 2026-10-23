from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

from google.cloud import speech_v1p1beta1 as speech


DEFAULT_LANGUAGE_CODE = os.getenv("GOOGLE_SPEECH_LANGUAGE_CODE", "en-US")
DEFAULT_MODEL = os.getenv("GOOGLE_SPEECH_MODEL", "latest_long")
DEFAULT_SAMPLE_RATE_HERTZ = int(os.getenv("GOOGLE_SPEECH_SAMPLE_RATE_HERTZ", "16000"))


@dataclass(frozen=True)
class SpeechClientSettings:
    language_code: str = DEFAULT_LANGUAGE_CODE
    enable_automatic_punctuation: bool = True
    interim_results: bool = True
    model: str = DEFAULT_MODEL
    sample_rate_hertz: int = DEFAULT_SAMPLE_RATE_HERTZ


def get_speech_client(client: Optional[speech.SpeechClient] = None) -> speech.SpeechClient:
    return client or speech.SpeechClient()


def get_speech_settings(
    language_code: Optional[str] = None,
    enable_automatic_punctuation: Optional[bool] = None,
    interim_results: Optional[bool] = None,
    model: Optional[str] = None,
    sample_rate_hertz: Optional[int] = None,
) -> SpeechClientSettings:
    return SpeechClientSettings(
        language_code=language_code or DEFAULT_LANGUAGE_CODE,
        enable_automatic_punctuation=True if enable_automatic_punctuation is None else enable_automatic_punctuation,
        interim_results=True if interim_results is None else interim_results,
        model=model or DEFAULT_MODEL,
        sample_rate_hertz=sample_rate_hertz or DEFAULT_SAMPLE_RATE_HERTZ,
    )


def build_recognition_config(settings: Optional[SpeechClientSettings] = None) -> speech.RecognitionConfig:
    config = settings or SpeechClientSettings()
    return speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=config.sample_rate_hertz,
        language_code=config.language_code,
        enable_automatic_punctuation=config.enable_automatic_punctuation,
        model=config.model,
    )


def build_streaming_config(settings: Optional[SpeechClientSettings] = None) -> speech.StreamingRecognitionConfig:
    config = settings or SpeechClientSettings()
    return speech.StreamingRecognitionConfig(
        config=build_recognition_config(config),
        interim_results=config.interim_results,
    )
