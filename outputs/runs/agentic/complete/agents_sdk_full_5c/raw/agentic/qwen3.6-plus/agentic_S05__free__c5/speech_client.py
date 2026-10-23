"""Local configuration and client helper utilities for Google Cloud Streaming Speech-to-Text."""

import os
from typing import Optional

from google.cloud import speech_v1p1beta1 as speech
from google.oauth2 import service_account


GOOGLE_CLOUD_SPEECH_HOST = "speech.googleapis.com"
GOOGLE_CLOUD_PROJECT_ENV = "GOOGLE_CLOUD_PROJECT"
GOOGLE_CREDENTIALS_ENV = "GOOGLE_APPLICATION_CREDENTIALS"


def get_credentials_path() -> Optional[str]:
    """Return the path to Google service account credentials."""
    return os.environ.get(GOOGLE_CREDENTIALS_ENV)


def get_project_id() -> Optional[str]:
    """Return the Google Cloud project ID."""
    return os.environ.get(GOOGLE_CLOUD_PROJECT_ENV)


def create_speech_client(
    credentials_path: Optional[str] = None,
) -> speech.SpeechClient:
    """Create a Google Cloud Speech-to-Text client for streaming recognition.

    Uses the google-cloud-speech SDK to connect to speech.googleapis.com.
    """
    if credentials_path:
        credentials = service_account.Credentials.from_service_account_file(
            credentials_path
        )
        return speech.SpeechClient(credentials=credentials)
    return speech.SpeechClient()


def build_streaming_config(
    encoding: speech.RecognitionConfig.AudioEncoding = speech.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz: int = 16000,
    language_code: str = "en-US",
    enable_automatic_punctuation: bool = True,
    model: str = "default",
    max_alternatives: int = 1,
    enable_word_time_offsets: bool = False,
    enable_interim_results: bool = True,
) -> speech.StreamingRecognitionConfig:
    """Build a StreamingRecognitionConfig for Google Cloud Speech-to-Text.

    Provider: Google Cloud Speech-to-Text (speech.googleapis.com)
    Models: 'default', 'command_and_search', 'phone_call', 'video', 'medical_conversation'
    """
    config = speech.RecognitionConfig(
        encoding=encoding,
        sample_rate_hertz=sample_rate_hertz,
        language_code=language_code,
        enable_automatic_punctuation=enable_automatic_punctuation,
        model=model,
        max_alternatives=max_alternatives,
        enable_word_time_offsets=enable_word_time_offsets,
    )
    return speech.StreamingRecognitionConfig(
        config=config,
        interim_results=enable_interim_results,
    )


def build_config_with_language(
    language_code: str = "en-US",
    alternative_language_codes: Optional[list[str]] = None,
    enable_automatic_punctuation: bool = True,
    enable_word_time_offsets: bool = True,
    model: str = "default",
    encoding: speech.RecognitionConfig.AudioEncoding = speech.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz: int = 16000,
) -> speech.StreamingRecognitionConfig:
    """Build a streaming config with explicit language and punctuation settings.

    Provider: Google Cloud Speech-to-Text (speech.googleapis.com)
    """
    kwargs = {
        "encoding": encoding,
        "sample_rate_hertz": sample_rate_hertz,
        "language_code": language_code,
        "enable_automatic_punctuation": enable_automatic_punctuation,
        "model": model,
        "enable_word_time_offsets": enable_word_time_offsets,
    }
    if alternative_language_codes:
        kwargs["alternative_language_codes"] = alternative_language_codes

    config = speech.RecognitionConfig(**kwargs)
    return speech.StreamingRecognitionConfig(
        config=config,
        interim_results=True,
    )
