import os
from .speech_client import SpeechClient
from .speech_models import TranscriptionResponse


def get_diarized_transcript(transcription_id: str) -> TranscriptionResponse:
    client = SpeechClient()
    response = client.get_diarized_transcript(transcription_id)
    if not response:
        raise ValueError("Diarized transcript not available")
    return response
