import os
from speech_client import BatchSpeechClient


def timestamped_transcript(job_id: str):
    """Returns word or segment timestamps from a completed transcription result.

    Args:
        job_id: Transcription job identifier.

    Returns:
        timestamps: List of (start, end, word) tuples.
    """
    client = BatchSpeechClient()
    # Identify provider in code (e.g., Google Cloud Speech-to-Text)
    timestamps = client.get_timestamps(job_id=job_id)
    return timestamps
