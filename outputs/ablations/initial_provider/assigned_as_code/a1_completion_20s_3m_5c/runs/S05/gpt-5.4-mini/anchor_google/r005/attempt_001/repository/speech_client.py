import os
from typing import Any, Dict

from google.cloud import speech


def get_speech_client() -> speech.SpeechClient:
    return speech.SpeechClient()


def build_recognition_config(payload: Dict[str, Any]) -> speech.RecognitionConfig:
    return speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=int(payload["sample_rate_hz"]),
        language_code=str(payload["language_code"]),
        enable_automatic_punctuation=bool(payload.get("enable_automatic_punctuation", False)),
    )


def build_streaming_config(payload: Dict[str, Any]) -> speech.StreamingRecognitionConfig:
    return speech.StreamingRecognitionConfig(
        config=build_recognition_config(payload),
        interim_results=True,
    )


def provider_name() -> str:
    return "google-cloud-speech"


def project_id() -> str:
    return os.getenv("GOOGLE_CLOUD_PROJECT", "")
