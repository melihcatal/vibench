import os
from .speech_client import AssemblyAISpeechClient
from .speech_models import TranscriptionRequest


def submit_transcription(audio_url: str) -> str:
    client = AssemblyAISpeechClient()
    request = TranscriptionRequest(audio_url=audio_url)
    return client.submit_transcription(request)
