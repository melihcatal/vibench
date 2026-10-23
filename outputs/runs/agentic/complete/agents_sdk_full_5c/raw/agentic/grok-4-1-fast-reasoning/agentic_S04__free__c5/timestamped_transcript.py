from typing import List

from speech_client import wait_for_completion, download_transcript_json
from speech_models import extract_words, TimestampedWord

def get_timestamped_words(job_name: str) -> List[TimestampedWord]:
    job = wait_for_completion(job_name)
    results = download_transcript_json(job)
    return extract_words(results)