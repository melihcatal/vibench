from typing import Optional

from speech_client import wait_for_completion, download_transcript_json
from speech_models import extract_transcript

def poll_transcription(job_name: str) -> str:
    job = wait_for_completion(job_name)
    results = download_transcript_json(job)
    return extract_transcript(results)