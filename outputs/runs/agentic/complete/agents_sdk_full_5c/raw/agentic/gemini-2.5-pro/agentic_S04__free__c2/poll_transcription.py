import time
from speech_client import assemblyai_client
from speech_models import TranscriptionJob, TranscriptionResult

def poll_transcription_job(job_id: str, timeout_seconds: int = 180, poll_interval: int = 5) -> TranscriptionResult:
    """
    Polls an AssemblyAI transcription job until it's completed or fails.

    Args:
        job_id: The ID of the transcription job to poll.
        timeout_seconds: Maximum time to wait for the job to complete.
        poll_interval: Time in seconds between polling attempts.

    Returns:
        The transcription result if the job completes successfully.
    
    Raises:
        TimeoutError: If the job does not complete within the specified timeout.
        Exception: If the job fails.
    """
    start_time = time.time()
    
    while time.time() - start_time < timeout_seconds:
        transcript = assemblyai_client.get_by_id(transcript_id=job_id)
        
        if transcript.status == 'completed':
            return TranscriptionResult(
                job_id=job_id,
                transcript_text=transcript.text
            )
        elif transcript.status == 'error':
            raise Exception(f"Transcription job {job_id} failed with error: {transcript.error}")
        
        time.sleep(poll_interval)
        
    raise TimeoutError(f"Transcription job {job_id} timed out after {timeout_seconds} seconds.")
