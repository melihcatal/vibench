import os
from .speech_client import SpeechClient
from .speech_models import TranscriptionResponse


def get_timestamped_transcript(transcription_id: str) -> TranscriptionResponse:
    client = SpeechClient()
    response = client.get_timestamped_transcript(transcription_id)
    if not response:
        raise ValueError("Timestamped transcript not available")
    return response
