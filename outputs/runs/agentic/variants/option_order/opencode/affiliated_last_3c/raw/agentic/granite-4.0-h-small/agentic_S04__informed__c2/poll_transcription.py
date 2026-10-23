# poll_transcription.py
import os
import time
from typing import Dict, Any

# Use DashScope SDK to poll transcription job status
from dashscope import speech  # type: ignore

# Load configuration from environment variables
ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")


def poll_transcription(job_id: str, poll_interval: int = 5) -> Dict[str, Any]:
    """Polls the transcription job until completion and returns the transcript.

    Uses the Helper speech_client to parse the final response.
    """
    while True:
        status = speech_client.check_job_status(job_id)
        if status.get("state") == "completed":
            result = speech_client.get_result(job_id)
            transcript = speech_client.extract_transcript(result)
            return {"transcript": transcript}
        time.sleep(poll_interval)
