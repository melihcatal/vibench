# [HELPER] speech_client.py
# Local configuration and client helper utilities for Text-to-Speech

import os
from google.cloud import texttospeech


def get_client() -> texttospeech.TextToSpeechClient:
    """Creates a Text-to-Speech client, using credentials from GOOGLE_APPLICATION_CREDENTIALS env var."""
    # Ensure credentials are available; you may also configure with service account JSON
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_path:
        raise RuntimeError(
            "Please set GOOGLE_APPLICATION_CREDENTIALS to point to a service account key JSON"
        )
    return texttospeech.TextToSpeechClient()
