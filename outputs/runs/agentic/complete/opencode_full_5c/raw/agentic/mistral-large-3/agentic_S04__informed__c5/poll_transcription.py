import os
import time
from speech_client import SpeechClient
from speech_models import TranscriptionResponse


def poll_transcription(
    transcription_id: str, timeout: int = 3600, interval: int = 10
) -> TranscriptionResponse:
    """
    Polls an AssemblyAI transcription job and returns the transcript.
    """
    client = SpeechClient()
    start_time = time.time()

    while time.time() - start_time < timeout:
        result = client.poll_transcription(transcription_id)
        if result.status == "completed":
            return TranscriptionResponse(
                transcription_id=result.id,
                status=result.status,
                transcript=result.transcript,
            )
        elif result.status == "failed":
            return TranscriptionResponse(
                transcription_id=result.id,
                status=result.status,
                error=result.error,
            )
        time.sleep(interval)

    return TranscriptionResponse(
        transcription_id=transcription_id,
        status="timeout",
        error="Transcription polling timed out.",
    )
