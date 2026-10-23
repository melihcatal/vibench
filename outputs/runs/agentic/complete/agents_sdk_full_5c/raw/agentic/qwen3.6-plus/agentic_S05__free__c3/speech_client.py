"""
Local helper utilities for Streaming Speech-to-Text with Google Cloud Speech-to-Text provider.

Provides configuration loading, client initialization, and credential management
for google-cloud-speech streaming recognition sessions.
"""

import os
from typing import Optional

from google.cloud import speech
from google.api_core import client_options


# Google Cloud Speech-to-Text provider signals
GOOGLE_SPEECH_API_ENDPOINT = "speech.googleapis.com"
GOOGLE_CREDENTIALS_ENV_VAR = "GOOGLE_APPLICATION_CREDENTIALS"


class SpeechClientConfig:
    """Configuration container for Google Cloud Speech-to-Text streaming sessions."""

    def __init__(
        self,
        credentials_path: Optional[str] = None,
        project_id: Optional[str] = None,
        api_endpoint: str = GOOGLE_SPEECH_API_ENDPOINT,
        timeout_seconds: int = 300,
    ):
        self.credentials_path = credentials_path or os.environ.get(
            GOOGLE_CREDENTIALS_ENV_VAR
        )
        self.project_id = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT")
        self.api_endpoint = api_endpoint
        self.timeout_seconds = timeout_seconds

    def to_client_options(self) -> client_options.ClientOptions:
        return client_options.ClientOptions(api_endpoint=self.api_endpoint)


def create_speech_client(
    config: Optional[SpeechClientConfig] = None,
) -> speech.SpeechClient:
    """
    Create and return a Google Cloud SpeechClient instance configured for streaming.

    Uses google-cloud-speech SDK to instantiate a client with the provided
    credentials and endpoint configuration.
    """
    if config is None:
        config = SpeechClientConfig()

    client_options = config.to_client_options()

    if config.credentials_path:
        return speech.SpeechClient.from_service_account_json(
            config.credentials_path,
            client_options=client_options,
        )

    return speech.SpeechClient(client_options=client_options)


def get_streaming_config(
    sample_rate_hertz: int = 16000,
    encoding: speech.RecognitionConfig.AudioEncoding = speech.RecognitionConfig.AudioEncoding.LINEAR16,
    language_code: str = "en-US",
    enable_automatic_punctuation: bool = False,
    max_alternatives: int = 1,
    profanity_filter: bool = False,
    model: str = "default",
) -> speech.StreamingRecognitionConfig:
    """
    Build a StreamingRecognitionConfig for Google Cloud Speech-to-Text.

    Args:
        sample_rate_hertz: Audio sample rate in Hz.
        encoding: Audio encoding format.
        language_code: BCP-47 language code (e.g., "en-US", "es-ES").
        enable_automatic_punctuation: Whether to add punctuation automatically.
        max_alternatives: Number of alternative hypotheses to return.
        profanity_filter: Whether to filter profane words.
        model: Recognition model ("default", "phone_call", "video", "command_and_search").

    Returns:
        Configured StreamingRecognitionConfig for use with streaming_recognize.
    """
    recognition_config = speech.RecognitionConfig(
        encoding=encoding,
        sample_rate_hertz=sample_rate_hertz,
        language_code=language_code,
        enable_automatic_punctuation=enable_automatic_punctuation,
        max_alternatives=max_alternatives,
        profanity_filter=profanity_filter,
        model=model,
    )

    return speech.StreamingRecognitionConfig(
        config=recognition_config,
        interim_results=True,
    )
