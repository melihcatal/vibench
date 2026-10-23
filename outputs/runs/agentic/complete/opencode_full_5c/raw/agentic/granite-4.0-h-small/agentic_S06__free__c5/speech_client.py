# [HELPER] speech_client.py

import os
from typing import Optional

# Provider: Google Cloud Text-to-Speech
try:
    from google.cloud import texttospeech_v1 as texttospeech  # type: ignore
except ImportError:
    raise RuntimeError(
        "Install the Google Cloud Text-to-Speech client library: `pip install google-cloud-texttospeech`"
    )

# Load credentials from environment variable (or set it before running)
CLIENT = None


def get_client() -> texttospeech.TextToSpeechClient:
    global CLIENT
    if CLIENT is None:
        if os.getenv("GOOGLE_APPLICATION_CREDENTIALS") is None:
            raise RuntimeError(
                "Set GOOGLE_APPLICATION_CREDENTIALS env var to point to service account JSON"
            )
        CLIENT = texttospeech.TextToSpeechClient()
    return CLIENT


def get_default_voice(language_code: str = "en-US") -> str:
    """Return the default voice name for a language (e.g., en-US)."""
    client = get_client()
    voices = client.list_voices(language=language_code).voices[0]
    return voices.name  # first voice == default
