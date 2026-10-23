import os
from dataclasses import dataclass

from google.cloud import speech

from speech_models import TranscriptionRequest


@dataclass
class SpeechClientConfig:
    language_code: str = "en-US"
    enable_punctuation: bool = True
    model: str = "latest_long"


def load_config() -> SpeechClientConfig:
    return SpeechClientConfig(
        language_code=os.getenv("SPEECH_LANGUAGE_CODE", "en-US"),
        enable_punctuation=os.getenv("SPEECH_ENABLE_PUNCTUATION", "true").lower()
        == "true",
        model=os.getenv("GOOGLE_SPEECH_MODEL", "latest_long"),
    )


def build_streaming_config(request: TranscriptionRequest) -> speech.RecognitionConfig:
    return speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        language_code=request.language_code,
        enable_automatic_punctuation=request.enable_punctuation,
        model="latest_long",
    )


def create_client() -> speech.SpeechClient:
    return speech.SpeechClient()
