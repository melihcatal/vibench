# [HELPER] speech_client.py
# Local helper utilities that provide configuration and client helpers for Text-to-Speech.

import os
from typing import Optional

# ---------- Configuration ----------
# Helper for client libraries that require API keys or environment variables.
# Example for ElevenLabs (provider identifiable by the key used here)
ELEVENLABS_API_KEY: Optional[str] = os.getenv("ELEVENLABS_API_KEY")
# If other providers are used elsewhere, define their keys similarly, e.g.:
# AZURE_SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY")
# AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
# -----------------------------------


def get_tts_config(provider: str) -> dict:
    """Return a minimal provider-specific configuration dictionary.

    Args:
        provider (str): Identifier such as 'ElevenLabs', 'Azure', 'AWS', etc.

    Returns:
        dict: Key-value pairs expected by the provider's API client.
    """
    if provider == "ElevenLabs":
        return {"api_key": ELEVENLABS_API_KEY}
    # Add additional providers when needed
    raise ValueError(f"Unsupported TTS provider: {provider}")
