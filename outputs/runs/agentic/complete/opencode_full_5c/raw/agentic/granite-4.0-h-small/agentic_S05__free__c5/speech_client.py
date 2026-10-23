# [HELPER] speech_client.py
# Local configuration and client helper utilities for Streaming Speech-to-Text
from typing import Any
from google.cloud import speech_v1p1beta1 as speech

# Provider identifiers for each helper function
PROVIDER = {
    "google": "google",
    "openai": "openai",
}


def get_speech_client(provider: str = "google") -> Any:
    """Return a configured client instance for the requested provider."""
    if provider == "google":
        # Google Cloud Speech-to-Text client
        return speech.SpeechClient()
    elif provider == "openai":
        # OpenAI client for Whisper streaming
        from openai import OpenAI

        return OpenAI()
    else:
        raise ValueError(f"Unsupported provider: {provider}")


def get_recognition_config(provider: str = "google") -> Any:
    """Return a RecognitionConfig (or equivalent) for the given provider."""
    if provider == "google":
        from google.cloud.speech_v1p1beta1 import RecognitionConfig
        from google.cloud.speech_v1p1beta1.enums import (
            AudioEncoding,
            SpeechContext,
        )

        return RecognitionConfig(
            encoding=AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code="en-US",
            enable_automatic_punctuation=True,
            speech_contexts=[SpeechContext(phrases=["weather", "news"])],
            continuous=True,
        )
    elif provider == "openai":
        # No config needed for Whisper streaming in this helper
        return None
    else:
        raise ValueError(f"Unsupported provider: {provider}")
