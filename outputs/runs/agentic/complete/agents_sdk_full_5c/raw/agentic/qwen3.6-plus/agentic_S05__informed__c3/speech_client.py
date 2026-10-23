"""
Local configuration and client helper utilities for Google Cloud Speech-to-Text streaming.

Provides credential loading, client initialization, and streaming configuration helpers.
Provider: Google Cloud Speech-to-Text
SDK: google-cloud-speech
Auth: GOOGLE_APPLICATION_CREDENTIALS
"""

import os
from typing import Optional

from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import types as speech_types


def load_google_credentials(
    credentials_path: Optional[str] = None,
) -> None:
    """Load Google Cloud credentials from environment or explicit path."""
    if credentials_path:
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
    creds_env = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if not creds_env:
        raise EnvironmentError(
            "GOOGLE_APPLICATION_CREDENTIALS environment variable must be set "
            "or credentials_path must be provided."
        )


def create_streaming_speech_client(
    credentials_path: Optional[str] = None,
) -> speech.SpeechClient:
    """
    Create and return a Google Cloud SpeechClient configured for streaming.

    Args:
        credentials_path: Optional path to Google service account JSON.

    Returns:
        Configured speech.SpeechClient instance.
    """
    load_google_credentials(credentials_path)
    return speech.SpeechClient()


def build_streaming_config(
    language_code: str = "en-US",
    sample_rate_hertz: int = 16000,
    encoding: speech_types.RecognitionConfig.AudioEncoding = speech_types.RecognitionConfig.AudioEncoding.LINEAR16,
    enable_automatic_punctuation: bool = True,
    interim_results: bool = True,
    max_alternatives: int = 1,
    model: str = "default",
    use_enhanced: bool = False,
) -> speech_types.StreamingRecognitionConfig:
    """
    Build a StreamingRecognitionConfig for Google Cloud Speech streaming.

    Args:
        language_code: BCP-47 language code (e.g., 'en-US', 'es-ES').
        sample_rate_hertz: Audio sample rate in Hz.
        encoding: Audio encoding format.
        enable_automatic_punctuation: Whether to add punctuation automatically.
        interim_results: Whether to return interim (partial) results.
        max_alternatives: Maximum number of alternative hypotheses to return.
        model: Speech recognition model to use.
        use_enhanced: Whether to use enhanced models.

    Returns:
        Configured StreamingRecognitionConfig instance.
    """
    recognition_config = speech_types.RecognitionConfig(
        encoding=encoding,
        sample_rate_hertz=sample_rate_hertz,
        language_code=language_code,
        enable_automatic_punctuation=enable_automatic_punctuation,
        max_alternatives=max_alternatives,
        model=model,
        use_enhanced=use_enhanced,
    )

    return speech_types.StreamingRecognitionConfig(
        config=recognition_config,
        interim_results=interim_results,
    )


def build_audio_content_request(
    audio_bytes: bytes,
) -> speech_types.StreamingRecognizeRequest:
    """
    Create a streaming recognize request containing audio content.

    Args:
        audio_bytes: Raw audio bytes to be recognized.

    Returns:
        StreamingRecognizeRequest with audio content.
    """
    return speech_types.StreamingRecognizeRequest(
        audio_content=audio_bytes,
    )


def streaming_generator_from_requests(
    requests: list[speech_types.StreamingRecognizeRequest],
):
    """
    Generator that yields streaming requests sequentially.

    Args:
        requests: List of StreamingRecognizeRequest objects.

    Yields:
        Individual StreamingRecognizeRequest objects.
    """
    for request in requests:
        yield request


def validate_google_credentials_set() -> bool:
    """Check if Google Cloud credentials are properly configured."""
    creds_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if creds_path and os.path.isfile(creds_path):
        return True
    return False
