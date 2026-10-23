import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional

from google.cloud import speech_v1p1beta1 as speech


@dataclass(frozen=True)
class SpeechClientConfig:
    project_id: Optional[str]
    language_code: str
    sample_rate_hz: int
    channels: int
    model: str
    enable_automatic_punctuation: bool
    interim_results: bool
    single_utterance: bool


def _env_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _env_int(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None or not value.strip():
        return default
    try:
        return int(value)
    except ValueError:
        return default


def load_speech_client_config() -> SpeechClientConfig:
    return SpeechClientConfig(
        project_id=os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCLOUD_PROJECT"),
        language_code=os.getenv("GOOGLE_CLOUD_SPEECH_LANGUAGE_CODE", "en-US"),
        sample_rate_hz=_env_int("GOOGLE_SPEECH_SAMPLE_RATE_HZ", 16000),
        channels=_env_int("GOOGLE_CLOUD_SPEECH_CHANNELS", 1),
        model=os.getenv("GOOGLE_CLOUD_SPEECH_MODEL", "latest_long"),
        enable_automatic_punctuation=_env_bool("GOOGLE_CLOUD_SPEECH_ENABLE_PUNCTUATION", True),
        interim_results=_env_bool("GOOGLE_CLOUD_SPEECH_INTERIM_RESULTS", True),
        single_utterance=_env_bool("GOOGLE_CLOUD_SPEECH_SINGLE_UTTERANCE", False),
    )


def build_recognition_config(language_code: Optional[str] = None, enable_punctuation: Optional[bool] = None) -> speech.RecognitionConfig:
    config = load_speech_client_config()
    return speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=config.sample_rate_hz,
        language_code=language_code or config.language_code,
        enable_automatic_punctuation=config.enable_automatic_punctuation if enable_punctuation is None else enable_punctuation,
        model=config.model,
        audio_channel_count=config.channels,
    )


def build_streaming_config(language_code: Optional[str] = None, enable_punctuation: Optional[bool] = None) -> speech.StreamingRecognitionConfig:
    config = load_speech_client_config()
    return speech.StreamingRecognitionConfig(
        config=build_recognition_config(language_code=language_code, enable_punctuation=enable_punctuation),
        interim_results=config.interim_results,
        single_utterance=config.single_utterance,
    )


@lru_cache(maxsize=1)
def get_speech_client() -> speech.SpeechClient:
    return speech.SpeechClient()


@lru_cache(maxsize=1)
def get_speech_async_client() -> speech.SpeechAsyncClient:
    return speech.SpeechAsyncClient()


def make_streaming_request(audio_content: bytes) -> speech.StreamingRecognizeRequest:
    return speech.StreamingRecognizeRequest(audio_content=audio_content)


__all__ = [
    "SpeechClientConfig",
    "build_recognition_config",
    "build_streaming_config",
    "get_speech_async_client",
    "get_speech_client",
    "load_speech_client_config",
    "make_streaming_request",
]
