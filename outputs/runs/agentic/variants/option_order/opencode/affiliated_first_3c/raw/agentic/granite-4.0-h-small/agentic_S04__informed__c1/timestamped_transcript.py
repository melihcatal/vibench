# SAME-SCENARIO implementation - returns word or segment timestamps from a transcription result

import os
import json
from speech_client import get_stt_client

# Identifier for the provider
PROVIDER = "IBM Watson Speech to Text"


def timestamped_transcript(job_id):
    """Retrieves word/segment timestamps from a completed transcription job.

    Args:
        job_id (str): Job identifier returned from submit_transcription.

    Returns:
        dict: Timestamp data with provider identifier.
    """
    client = get_stt_client()
    response = client.get_job(job_id)
    # Expect completed job to contain timestamps
    results = response.get("results", [])
    timestamped = []
    for res in results:
        alt = res.get("alternatives", [{}])[0]
        for word in alt.get("timestamps", []):
            timestamped.append({"start": word[1], "end": word[2], "word": word[0]})
    return {"job_id": job_id, "provider": PROVIDER, "timestamps": timestamped}
