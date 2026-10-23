import time
from speech_client import get_client
from speech_models import get_transcript

def poll_transcription(job_id: str, poll_interval: int = 5, max_wait_seconds: int = 3600) -> str:
    client = get_client()
    job = client.jobs.get(job_id)
    elapsed = 0
    while job.status not in ["completed", "error"]:
        time.sleep(poll_interval)
        elapsed += poll_interval
        if elapsed > max_wait_seconds:
            raise TimeoutError(f"Polling timed out after {max_wait_seconds} seconds")
        job = client.jobs.get(job_id)
    if job.status == "error":
        raise ValueError(f"Transcription job error: {getattr(job, 'error', 'Unknown error')}")
    transcript = get_transcript(job)
    if transcript is None:
        raise ValueError("No transcript in completed job")
    return transcript