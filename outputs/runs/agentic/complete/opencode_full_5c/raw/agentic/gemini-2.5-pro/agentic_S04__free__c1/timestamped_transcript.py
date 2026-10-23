from speech_client import SpeechClient
from typing import List, Dict, Any


def get_word_timestamps(job_id: str) -> List[Dict[str, Any]]:
    """
    Returns word timestamps from an AssemblyAI transcription result.
    """
    client = SpeechClient()
    response = client.get_job(job_id)
    if response.get("status") == "completed":
        return response.get("words", [])
    return []


def submit_for_timestamps(audio_url: str) -> str:
    """
    Submits a job to AssemblyAI, timestamps are returned by default.
    """
    client = SpeechClient()
    # Timestamps are enabled by default in AssemblyAI API v2
    response = client.submit_job(audio_url)
    return response.get("id")
