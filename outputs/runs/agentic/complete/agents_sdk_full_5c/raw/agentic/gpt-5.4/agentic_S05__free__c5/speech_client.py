import os
from typing import Optional

from google.cloud import speech_v2

DEFAULT_RECOGNIZER = os.getenv("GOOGLE_SPEECH_RECOGNIZER", "_")
DEFAULT_LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "global")
DEFAULT_PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "")


def get_speech_client() -> speech_v2.SpeechAsyncClient:
    return speech_v2.SpeechAsyncClient()


def get_recognizer_path(
    project_id: Optional[str] = None,
    location: Optional[str] = None,
    recognizer: Optional[str] = None,
) -> str:
    project = project_id or DEFAULT_PROJECT_ID
    if not project:
        raise ValueError("GOOGLE_CLOUD_PROJECT is required")
    loc = location or DEFAULT_LOCATION
    rec = recognizer or DEFAULT_RECOGNIZER
    return f"projects/{project}/locations/{loc}/recognizers/{rec}"


def get_streaming_endpoint_hint() -> str:
    return "speech.googleapis.com"
