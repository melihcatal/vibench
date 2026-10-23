from typing import List
from speech_client import get_from_assemblyai
from speech_models import TranscriptionJob, WordTimestamp

def get_timestamped_words(job_id: str) -> List[WordTimestamp]:
    """
    Retrieves a completed AssemblyAI transcript and extracts word-level timestamps.
    Assumes the job is already completed.
    """
    response_data = get_from_assemblyai(f"transcript/{job_id}")
    job = TranscriptionJob(**response_data)

    if job.status != "completed":
        raise ValueError(f"Job {job_id} is not complete. Current status: {job.status}")

    if not job.words:
        return []

    return [WordTimestamp(**word) for word in job.words]
