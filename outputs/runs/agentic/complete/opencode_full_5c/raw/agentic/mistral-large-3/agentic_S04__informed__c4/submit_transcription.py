import os
from .speech_client import TranscriptionClient
from .speech_models import TranscriptionRequest


def submit_transcription(audio_url: str, language_code: str = "en") -> str:
    client = TranscriptionClient()
    request = TranscriptionRequest(audio_url=audio_url, language_code=language_code)
    return client.submit_transcription(request)
