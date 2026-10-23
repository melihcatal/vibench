# timestamped_transcript.py
import os
from typing import Dict, Any

# Use DashScope SDK to obtain word/segment timestamps from a completed transcription result
from dashscope import speech  # type: ignore

# Load configuration from environment variables
ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")


def timestamped_transcript(job_id: str) -> Dict[str, Any]:
    """Retrieves word or segment timestamps for a transcription job.

    Uses the Helper speech_client to extract timing information from the provider result.
    """
    raw = assemblyai_client.get_transcription_result(job_id)
    timestamps = speech_client.parse_timestamps(raw)
    return {"timestamps": timestamps}
