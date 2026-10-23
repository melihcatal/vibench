import os
import time
from .speech_client import TranscriptionClient
from .speech_models import TranscriptionResponse


def poll_transcription(
    transcription_id: str, max_attempts: int = 30, delay: int = 10
) -> TranscriptionResponse:
    client = TranscriptionClient()
    for _ in range(max_attempts):
        response = client.get_transcription(transcription_id)
        if response and response.status == "completed":
            return response
        time.sleep(delay)
    raise TimeoutError("Transcription polling timed out")
