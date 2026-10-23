"""Local configuration and client helper utilities for Batch Speech-to-Text using AssemblyAI."""

import os
from typing import Optional

import assemblyai


def get_assemblyai_client(api_key: Optional[str] = None) -> assemblyai.Client:
    """Create and return an AssemblyAI client using the provider SDK.

    Uses ASSEMBLYAI_API_KEY environment variable if api_key is not provided.
    """
    key = api_key or os.environ.get("ASSEMBLYAI_API_KEY")
    if not key:
        raise ValueError("ASSEMBLYAI_API_KEY environment variable is required")
    return assemblyai.Client(api_key=key)


def get_default_settings() -> dict:
    """Return default transcription settings for AssemblyAI batch jobs."""
    return {
        "language_code": "en_us",
        "punctuate": True,
        "format_text": True,
    }


def normalize_audio_source(audio_path: Optional[str] = None, audio_url: Optional[str] = None) -> str:
    """Normalize audio source into a format AssemblyAI accepts.

    Returns a URL if provided, otherwise returns the local file path
    which AssemblyAI SDK handles by uploading automatically.
    """
    if audio_url:
        return audio_url
    if audio_path:
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        return audio_path
    raise ValueError("Either audio_path or audio_url must be provided")
