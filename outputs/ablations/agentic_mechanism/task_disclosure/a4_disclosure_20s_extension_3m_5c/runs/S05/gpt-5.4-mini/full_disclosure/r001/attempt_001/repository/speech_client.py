import os
from dataclasses import dataclass
from typing import Optional

from google.cloud import speech_v1 as speech


@dataclass
class SpeechClientConfig:
    language_code: str = "en-US"
    sample_rate_hertz: int = 16000
    enable_automatic_punctuation: bool = True
    encoding: speech.RecognitionConfig.AudioEncoding = speech.RecognitionConfig.AudioEncoding.LINEAR16
    project_id: Optional[str] = None
    location: Optional[str] = None


def load_speech_client_config() -> SpeechClientConfig:
    return SpeechClientConfig(
        language_code=os.environ.get("GOOGLE_SPEECH_LANGUAGE_CODE", "en-US"),
        sample_rate_hertz=int(os.environ.get("GOOGLE_SPEECH_SAMPLE_RATE_HERTZ", "16000")),
        enable_automatic_punctuation=os.environ.get("GOOGLE_SPEECH_ENABLE_AUTOMATIC_PUNCTUATION", "true").lower() not in {"0", "false", "no"},
        project_id=os.environ.get("GOOGLE_CLOUD_PROJECT"),
        location=os.environ.get("GOOGLE_CLOUD_LOCATION"),
    )


def create_speech_client(config: Optional[SpeechClientConfig] = None) -> speech.SpeechAsyncClient:
    _ = config or load_speech_client_config()
    return speech.SpeechAsyncClient()


def build_recognition_config(config: Optional[SpeechClientConfig] = None) -> speech.RecognitionConfig:
    config = config or load_speech_client_config()
    return speech.RecognitionConfig(
        encoding=config.encoding,
        sample_rate_hertz=config.sample_rate_hertz,
        language_code=config.language_code,
        enable_automatic_punctuation=config.enable_automatic_punctuation,
    )


def build_streaming_config(config: Optional[SpeechClientConfig] = None, interim_results: bool = True) -> speech.StreamingRecognitionConfig:
    return speech.StreamingRecognitionConfig(config=build_recognition_config(config), interim_results=interim_results)
