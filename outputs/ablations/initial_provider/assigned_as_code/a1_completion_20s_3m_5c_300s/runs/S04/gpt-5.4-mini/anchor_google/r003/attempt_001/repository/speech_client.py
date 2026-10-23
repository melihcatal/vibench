import os
from typing import Any, Dict

from google.cloud import speech


def get_default_language() -> str:
    return os.getenv("GOOGLE_CLOUD_SPEECH_LANGUAGE_CODE", "en-US")


def get_client() -> speech.SpeechClient:
    return speech.SpeechClient()


def build_recognition_config(payload: Dict[str, Any]) -> speech.RecognitionConfig:
    return speech.RecognitionConfig(
        language_code=payload.get("language_code", get_default_language()),
        enable_speaker_diarization=payload.get("diarization", False),
        enable_word_time_offsets=payload.get("enable_word_time_offsets", False),
        model=payload.get("model"),
    )
