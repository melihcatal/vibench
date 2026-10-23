# SAME-SCENARIO: poll_transcription.py

# Integration with AssemblyAI Transcripts API
# Provider: AssemblyAI (ASSEMBLYAI_API_KEY environment variable)
import os
import time
import requests

API_URL = "https://api.assemblyai.com/v2/transcript"
API_KEY = os.getenv("ASSEMBLYAI_API_KEY")

def poll_transcription(job_id: str, poll_interval: float = 1.0) -> dict:
    """Poll AssemblyAI for transcription result.

    Args:
        job_id: Transcription job ID returned from submit_transcription.
        poll_interval: Seconds to wait between status checks (default: 1.0).

    Returns:
        JSON response containing the final transcript when the job completes.
    """
    if not API_KEY:
        raise RuntimeError("ASSEMBLYAI_API_KEY environment variable not set.")

    while True:
        headers = {"Authorization": API_KEY}
        resp = requests.get(f"{API_URL}/{job_id}", headers=headers)
        resp.raise_for_status()
        data = resp.json()
        if data["status"] == "completed":
            return data
        elif data["status"] == "error":
            raise RuntimeError(f"Transcription failed: {data.get('error')}"),
        time.sleep(poll_interval)
