import os
import time
from .speech_client import SpeechClient
from .speech_models import TranscriptionResponse


def poll_transcription(
    transcription_id: str, max_attempts: int = 30, delay: int = 10
) -> TranscriptionResponse:
    client = SpeechClient()
    for _ in range(max_attempts):
        response = client.poll_transcription(transcription_id)
        if response:
            return response
        time.sleep(delay)
    raise TimeoutError("Transcription polling timed out")
