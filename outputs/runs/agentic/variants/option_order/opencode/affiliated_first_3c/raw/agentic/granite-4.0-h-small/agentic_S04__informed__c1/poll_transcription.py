# SAME-SCENARIO implementation - polls a transcription job and returns the transcript

import os
import json
from speech_client import get_stt_client

# Identifier for the provider
PROVIDER = "IBM Watson Speech to Text"


def poll_transcription(job_id):
    """Polls a transcription job and returns the complete transcript.

    Args:
        job_id (str): Job identifier returned from submit_transcription.

    Returns:
        dict: Transcription result with provider identifier and transcript text.
    """
    client = get_stt_client()
    # Poll until job is completed (simplified linear poll)
    while True:
        response = client.get_job(job_id)
        status = response.get("status", "").lower()
        if status == "completed":
            transcript = response.get("results", [{}])[0].get("transcript", "")
            return {
                "job_id": job_id,
                "status": status,
                "provider": PROVIDER,
                "transcript": transcript,
            }
        elif status == "failed":
            raise RuntimeError(f"Transcription job failed: {response.get('error')}")
        # Wait and retry (simple sleep)
        import time

        time.sleep(2)
