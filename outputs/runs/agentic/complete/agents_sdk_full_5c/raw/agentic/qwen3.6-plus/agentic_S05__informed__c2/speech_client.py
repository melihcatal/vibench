"""
Local configuration and client helper utilities for Google Cloud Streaming Speech-to-Text.
Provides client initialization, credential loading, and streaming configuration helpers.
"""

import os
from typing import Optional

from google.cloud import speech_v1p1beta1 as speech
from google.oauth2 import service_account


def load_credentials_from_env() -> Optional[service_account.Credentials]:
    """Load Google service account credentials from GOOGLE_APPLICATION_CREDENTIALS."""
    credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if credentials_path and os.path.isfile(credentials_path):
        return service_account.Credentials.from_service_account_file(credentials_path)
    return None


def create_speech_client(
    credentials_path: Optional[str] = None,
) -> speech.SpeechClient:
    """
    Create a Google Cloud Speech-to-Text client.

    Args:
        credentials_path: Optional path to a service account JSON file.
                          Falls back to GOOGLE_APPLICATION_CREDENTIALS env var.

    Returns:
        Configured google.cloud.speech_v1p1beta1.SpeechClient instance.
    """
    if credentials_path and os.path.isfile(credentials_path):
        credentials = service_account.Credentials.from_service_account_file(
            credentials_path
        )
        return speech.SpeechClient(credentials=credentials)

    return speech.SpeechClient()


def build_streaming_config(
    sample_rate_hertz: int = 16000,
    language_code: str = "en-US",
    enable_automatic_punctuation: bool = True,
    encoding: speech.RecognitionConfig.AudioEncoding = speech.RecognitionConfig.AudioEncoding.LINEAR16,
    max_alternatives: int = 1,
    enable_word_time_offsets: bool = True,
    interim_results: bool = True,
) -> speech.StreamingRecognitionConfig:
    """
    Build a StreamingRecognitionConfig for Google Cloud Speech streaming.

    Args:
        sample_rate_hertz: Audio sample rate.
        language_code: BCP-47 language code (e.g., 'en-US', 'es-ES').
        enable_automatic_punctuation: Whether to add punctuation automatically.
        encoding: Audio encoding format.
        max_alternatives: Number of alternative hypotheses to return.
        enable_word_time_offsets: Whether to return word-level timing.
        interim_results: Whether to return interim (partial) results.

    Returns:
        Configured StreamingRecognitionConfig.
    """
    config = speech.RecognitionConfig(
        encoding=encoding,
        sample_rate_hertz=sample_rate_hertz,
        language_code=language_code,
        enable_automatic_punctuation=enable_automatic_punctuation,
        max_alternatives=max_alternatives,
        enable_word_time_offsets=enable_word_time_offsets,
    )
    return speech.StreamingRecognitionConfig(
        config=config,
        interim_results=interim_results,
    )


def build_streaming_config_with_alternate_languages(
    sample_rate_hertz: int = 16000,
    language_code: str = "en-US",
    alternate_language_codes: Optional[list[str]] = None,
    enable_automatic_punctuation: bool = True,
    encoding: speech.RecognitionConfig.AudioEncoding = speech.RecognitionConfig.AudioEncoding.LINEAR16,
    max_alternatives: int = 1,
    enable_word_time_offsets: bool = True,
    interim_results: bool = True,
) -> speech.StreamingRecognitionConfig:
    """
    Build a StreamingRecognitionConfig with alternate language support.

    Args:
        sample_rate_hertz: Audio sample rate.
        language_code: Primary BCP-47 language code.
        alternate_language_codes: List of alternate language codes.
        enable_automatic_punctuation: Whether to add punctuation automatically.
        encoding: Audio encoding format.
        max_alternatives: Number of alternative hypotheses to return.
        enable_word_time_offsets: Whether to return word-level timing.
        interim_results: Whether to return interim (partial) results.

    Returns:
        Configured StreamingRecognitionConfig with alternate languages.
    """
    config_kwargs = {
        "encoding": encoding,
        "sample_rate_hertz": sample_rate_hertz,
        "language_code": language_code,
        "enable_automatic_punctuation": enable_automatic_punctuation,
        "max_alternatives": max_alternatives,
        "enable_word_time_offsets": enable_word_time_offsets,
    }
    if alternate_language_codes:
        config_kwargs["alternative_language_codes"] = alternate_language_codes

    config = speech.RecognitionConfig(**config_kwargs)
    return speech.StreamingRecognitionConfig(
        config=config,
        interim_results=interim_results,
    )
