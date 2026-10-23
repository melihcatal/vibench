import os
from .speech_client import SpeechClient
from .speech_models import TranscriptionRequest


def submit_transcription(audio_url: str) -> dict:
    client = SpeechClient()
    request = TranscriptionRequest(audio_url=audio_url)
    response = client.submit_transcription(request)
    return response
