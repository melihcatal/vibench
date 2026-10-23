"""Local configuration and client helper utilities for Streaming Speech-to-Text."""

import os
from typing import Optional, Dict, Any
from google.cloud import speech_v2
from google.cloud.speech_v2 import SpeechClient
from google.oauth2 import service_account


GOOGLE_SPEECH_ENDPOINT = os.environ.get(
    "GOOGLE_SPEECH_ENDPOINT",
    "speech.googleapis.com"
)

DEFAULT_PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "")
DEFAULT_LOCATION = "global"
DEFAULT_RECOGNIZER_ID = "_"


def build_recognizer_path(
    project_id: Optional[str] = None,
    location: str = DEFAULT_LOCATION,
    recognizer_id: str = DEFAULT_RECOGNIZER_ID,
) -> str:
    """Build the full recognizer resource path for Google Cloud Speech-to-Text v2."""
    pid = project_id or DEFAULT_PROJECT_ID
    return f"projects/{pid}/locations/{location}/recognizers/{recognizer_id}"


def get_speech_client(
    credentials_path: Optional[str] = None,
    endpoint: Optional[str] = None,
) -> SpeechClient:
    """Create and return a Google Cloud SpeechClient for streaming recognition."""
    client_kwargs: Dict[str, Any] = {}
    if endpoint:
        client_kwargs["client_options"] = {"api_endpoint": endpoint}
    elif GOOGLE_SPEECH_ENDPOINT:
        client_kwargs["client_options"] = {"api_endpoint": GOOGLE_SPEECH_ENDPOINT}

    if credentials_path:
        credentials = service_account.Credentials.from_service_account_file(credentials_path)
        client_kwargs["credentials"] = credentials

    return SpeechClient(**client_kwargs)


def get_speech_config(
    language_codes: list[str] | None = None,
    model: str = "latest_long",
    enable_automatic_punctuation: bool = True,
    enable_word_time_offsets: bool = True,
    max_alternatives: int = 1,
) -> dict:
    """Return default streaming speech configuration."""
    return {
        "language_codes": language_codes or ["en-US"],
        "model": model,
        "enable_automatic_punctuation": enable_automatic_punctuation,
        "enable_word_time_offsets": enable_word_time_offsets,
        "max_alternatives": max_alternatives,
    }
