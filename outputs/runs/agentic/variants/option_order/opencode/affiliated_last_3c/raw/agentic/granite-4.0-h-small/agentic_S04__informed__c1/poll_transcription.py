import os
from speech_client import BatchSpeechClient


def poll_transcription(job_id: str, timeout_seconds: int = 300):
    """Polls a batch transcription job and returns the completed transcript.

    Args:
        job_id: The job identifier returned by submit_transcription.
        timeout_seconds: How long to wait for completion before raising TimeoutError.

    Returns:
        transcript: Final transcript text.
    """
    client = BatchSpeechClient()
    # Identify provider in code (e.g., Amazon Transcribe)
    transcript = client.get_transcription_result(job_id=job_id, timeout=timeout_seconds)
    return transcript
