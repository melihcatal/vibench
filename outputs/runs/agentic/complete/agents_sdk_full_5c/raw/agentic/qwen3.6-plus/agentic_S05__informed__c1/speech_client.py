"""
Local configuration and client helper utilities for Streaming Speech-to-Text.

Provides Deepgram API configuration loading, authentication helpers,
and streaming client initialization utilities.
"""

import os
from typing import Optional, Dict, Any


def load_deepgram_config() -> Dict[str, str]:
    """Load Deepgram API configuration from environment variables.

    Returns:
        Dictionary containing API key and optional API URL.

    Raises:
        ValueError: If DEEPGRAM_API_KEY is not set.
    """
    api_key = os.environ.get("DEEPGRAM_API_KEY")
    if not api_key:
        raise ValueError("DEEPGRAM_API_KEY environment variable is required")

    api_url = os.environ.get(
        "DEEPGRAM_API_URL", "https://api.deepgram.com/v1/listen"
    )

    return {
        "api_key": api_key,
        "api_url": api_url,
    }


def build_deepgram_client(api_key: Optional[str] = None):
    """Build a Deepgram streaming client using the deepgram-sdk.

    Args:
        api_key: Deepgram API key. If not provided, reads from DEEPGRAM_API_KEY.

    Returns:
        Configured DeepgramClient instance for streaming transcription.
    """
    from deepgram import DeepgramClient, DeepgramClientOptions

    key = api_key or os.environ.get("DEEPGRAM_API_KEY")
    if not key:
        raise ValueError("DEEPGRAM_API_KEY environment variable is required")

    options = DeepgramClientOptions(
        options={"keepalive": "true"},
    )

    client = DeepgramClient(api_key=key, config=options)
    return client


def get_default_streaming_options(
    model: str = "nova-2",
    language: str = "en",
    smart_format: bool = True,
    interim_results: bool = True,
    punctuate: bool = True,
    encoding: str = "linear16",
    sample_rate: int = 16000,
    channels: int = 1,
) -> Dict[str, Any]:
    """Get default streaming options for Deepgram real-time transcription.

    Args:
        model: Deepgram model identifier (e.g., 'nova-2', 'nova-2-general').
        language: Language code for transcription.
        smart_format: Enable smart formatting of output.
        interim_results: Whether to return interim results.
        punctuate: Whether to add punctuation to transcripts.
        encoding: Audio encoding format.
        sample_rate: Audio sample rate in Hz.
        channels: Number of audio channels.

    Returns:
        Dictionary of Deepgram streaming options.
    """
    return {
        "model": model,
        "language": language,
        "smart_format": smart_format,
        "interim_results": interim_results,
        "punctuate": punctuate,
        "encoding": encoding,
        "sample_rate": sample_rate,
        "channels": channels,
    }


def validate_audio_params(
    sample_rate: int = 16000,
    channels: int = 1,
    encoding: str = "linear16",
) -> None:
    """Validate audio parameters for Deepgram streaming.

    Args:
        sample_rate: Audio sample rate in Hz.
        channels: Number of audio channels.
        encoding: Audio encoding format.

    Raises:
        ValueError: If parameters are invalid for Deepgram streaming.
    """
    supported_rates = [8000, 16000, 24000, 32000, 44100, 48000]
    supported_encodings = ["linear16", "mulaw", "alaw", "flac", "opus"]

    if sample_rate not in supported_rates:
        raise ValueError(
            f"Unsupported sample rate {sample_rate}. "
            f"Supported: {supported_rates}"
        )

    if encoding not in supported_encodings:
        raise ValueError(
            f"Unsupported encoding '{encoding}'. "
            f"Supported: {supported_encodings}"
        )

    if channels < 1 or channels > 2:
        raise ValueError(f"Channels must be 1 or 2, got {channels}")
