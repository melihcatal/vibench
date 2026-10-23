from speech_client import SpeechClient
from speech_models import TimestampedTranscriptionResponse
from typing import Optional


def get_timestamped_transcript(
    job_id: str,
) -> Optional[TimestampedTranscriptionResponse]:
    """
    Returns word timestamps from an AssemblyAI transcription result.
    """
    client = SpeechClient()
    response = client.get_timestamped_transcript(job_id)
    return response
