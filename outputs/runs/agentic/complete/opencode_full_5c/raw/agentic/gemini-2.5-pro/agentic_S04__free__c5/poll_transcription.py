import time
import os
from speech_client import get_transcript


def poll_transcription_job(job_id: str) -> str:
    """
    Polls a transcription job from AssemblyAI and returns the transcript.
    """
    if not os.getenv("ASSEMBLYAI_API_KEY"):
        raise EnvironmentError("ASSEMBLYAI_API_KEY environment variable not set.")

    while True:
        result = get_transcript(job_id)
        if result["status"] == "completed":
            return result["text"]
        elif result["status"] == "failed":
            return "Transcription failed."
        time.sleep(5)
