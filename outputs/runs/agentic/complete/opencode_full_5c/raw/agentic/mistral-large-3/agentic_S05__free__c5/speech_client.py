import os
from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import types
from typing import Optional


def get_speech_client() -> speech.SpeechClient:
    """Initializes and returns a Google Cloud Speech-to-Text client."""
    return speech.SpeechClient()


def load_config_from_env() -> dict:
    """Loads configuration from environment variables."""
    return {
        "project_id": os.getenv("GOOGLE_CLOUD_PROJECT_ID"),
        "language_code": os.getenv("SPEECH_LANGUAGE_CODE", "en-US"),
        "model": os.getenv("SPEECH_MODEL", "latest_long"),
        "sample_rate_hertz": int(os.getenv("SPEECH_SAMPLE_RATE_HERTZ", "16000")),
    }
