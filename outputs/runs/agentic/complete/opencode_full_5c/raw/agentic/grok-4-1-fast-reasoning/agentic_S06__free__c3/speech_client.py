import os
from typing import Optional

from google.cloud import texttospeech
from google.cloud import storage

_tts_client: Optional[texttospeech.TextToSpeechClient] = None
_storage_client: Optional[storage.Client] = None


def get_tts_client() -> texttospeech.TextToSpeechClient:
    global _tts_client
    if _tts_client is None:
        _tts_client = texttospeech.TextToSpeechClient()
    return _tts_client


def get_storage_client() -> storage.Client:
    global _storage_client
    if _storage_client is None:
        project = os.getenv("GOOGLE_CLOUD_PROJECT")
        if project is None:
            raise ValueError("GOOGLE_CLOUD_PROJECT environment variable is required")
        _storage_client = storage.Client(project=project)
    return _storage_client
