from speech_client import get_client
from speech_models import get_word_timestamps

def timestamped_transcript(job_id: str) -> list[dict]:
    client = get_client()
    job = client.jobs.get(job_id)
    if not hasattr(job, 'status') or job.status != "completed":
        raise ValueError(f"Job must be completed, status: {getattr(job, 'status', 'unknown')}")
    return get_word_timestamps(job)