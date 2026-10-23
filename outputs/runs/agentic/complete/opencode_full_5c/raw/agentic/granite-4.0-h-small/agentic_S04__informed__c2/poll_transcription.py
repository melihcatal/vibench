import time
import os
import json
from assemblyai import AssemblyAI

# Load API key from environment
ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")

# Initialize client once per process
aai = AssemblyAI(ASSEMBLYAI_API_KEY)


def poll_transcription(job_id: str, poll_interval: int = 5) -> dict:
    """Poll a transcription job until it is completed.
    Returns the final transcript JSON response.
    """
    while True:
        result = aai.transcript.poll(job_id)
        status = result.get("status", "pending")
        if status in ["completed", "failed"]:
            return result
        time.sleep(poll_interval)
