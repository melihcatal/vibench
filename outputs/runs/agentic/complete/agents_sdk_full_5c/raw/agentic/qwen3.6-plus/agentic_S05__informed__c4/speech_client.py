"""Local configuration and client helper utilities for Deepgram Streaming Speech-to-Text."""

import os
from typing import Any

from deepgram import DeepgramClient, LiveOptions, PrerecordedOptions


DEEPGRAM_API_ENV = "DEEPGRAM_API_KEY"

DEFAULT_MODEL = "nova-2"
DEFAULT_LANGUAGE = "en"
DEFAULT_SAMPLE_RATE = 16000
DEFAULT_CHANNELS = 1


def get_deepgram_api_key() -> str:
    """Retrieve the Deepgram API key from environment variables."""
    api_key = os.environ.get(DEEPGRAM_API_ENV)
    if not api_key:
        raise EnvironmentError(
            f"Environment variable {DEEPGRAM_API_ENV} is not set. "
            "Please configure your Deepgram API key."
        )
    return api_key


def create_deepgram_client(api_key: str | None = None) -> DeepgramClient:
    """Create a DeepgramClient instance for streaming speech recognition."""
    resolved_key = api_key or get_deepgram_api_key()
    return DeepgramClient(resolved_key)


def build_live_options(
    model: str = DEFAULT_MODEL,
    language: str = DEFAULT_LANGUAGE,
    sample_rate: int = DEFAULT_SAMPLE_RATE,
    channels: int = DEFAULT_CHANNELS,
    interim_results: bool = True,
    punctuate: bool = True,
    smart_format: bool = True,
    **extra_kwargs: Any,
) -> LiveOptions:
    """Build Deepgram LiveOptions for a streaming session."""
    return LiveOptions(
        model=model,
        language=language,
        sample_rate=sample_rate,
        channels=channels,
        interim_results=interim_results,
        punctuate=punctuate,
        smart_format=smart_format,
        **extra_kwargs,
    )


def build_prerecorded_options(
    model: str = DEFAULT_MODEL,
    language: str = DEFAULT_LANGUAGE,
    punctuate: bool = True,
    **extra_kwargs: Any,
) -> PrerecordedOptions:
    """Build Deepgram PrerecordedOptions for batch transcription."""
    return PrerecordedOptions(
        model=model,
        language=language,
        punctuate=punctuate,
        **extra_kwargs,
    )
