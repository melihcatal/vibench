import os
time
from speech_client import BatchSpeechClient
from speech_models import TranscriptionJobResponse

def poll_transcription(job_id: str, timeout_minutes: int = 30) -> str:
    """Poll a batch transcription job until completion and return the full transcript.

    Args:
        job_id: The job identifier returned by submit_transcription.
        timeout_minutes: How long to wait before giving up.

    Returns:
        The final transcript text (plain string) once the job status is SUCCESS.
    """
    client = BatchSpeechClient()
    start = time.time()
    while True:
        status = client.get_transcription_job_status(job_id)
        if status == 'SUCCESS':
            result = client.get_transcription_job_result(job_id)
            # Normalize via local helpers
            return TranscriptionJobResponse.normalize(result)
        elif status == 'FAILED':
            raise RuntimeError('Transcription job failed')
        elif time.time() - start > timeout_minutes * 60:
            raise TimeoutError('Polling timed out')
        time.sleep(5)  # simple back‑off
