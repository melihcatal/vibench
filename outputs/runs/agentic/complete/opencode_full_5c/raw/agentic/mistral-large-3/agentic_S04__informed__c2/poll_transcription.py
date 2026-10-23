import os
from typing import Dict, Any
from .speech_client import AssemblyAISpeechClient
from .speech_models import TranscriptionResponse


def poll_transcription(transcription_id: str) -> TranscriptionResponse:
    client = AssemblyAISpeechClient()
    return client.poll_transcription(transcription_id)
