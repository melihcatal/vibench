import os
from speech_client import BatchSpeechClient


def timestamped_transcript(job_id: str) -> list:
    """Retrieve word-level timestamps for a completed transcription.

    Returns a list of dicts with start/end times and text.
    """
    client = BatchSpeechClient()
    result = client.get_transcription(job_id=job_id)
    # Assume `result.data` provides timestamps when transcription is complete
    return result.data.timestamps
