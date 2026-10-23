import time
from speech_client import get_from_assemblyai
from speech_models import TranscriptionJob

def poll_for_transcript(job_id: str) -> TranscriptionJob:
    """
    Polls AssemblyAI for the status of a transcription job and returns the result.
    """
    while True:
        response_data = get_from_assemblyai(f"transcript/{job_id}")
        job = TranscriptionJob(**response_data)
        
        if job.status == "completed":
            return job
        elif job.status == "error":
            raise Exception(f"Transcription failed: {job.error}")
        
        time.sleep(5)
