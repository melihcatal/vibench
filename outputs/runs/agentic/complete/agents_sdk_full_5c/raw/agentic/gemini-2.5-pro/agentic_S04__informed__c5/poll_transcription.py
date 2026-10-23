import time
from typing import Optional

from speech_client import get_speech_client
from speech_models import TranscriptionResult


def poll_transcription_job(job_id: str, timeout: int = 300, interval: int = 5) -> Optional[str]:
    """
    Polls an AssemblyAI transcription job until it's completed.

    Args:
        job_id: The ID of the transcription job to poll.
        timeout: The maximum time to wait in seconds.
        interval: The polling interval in seconds.

    Returns:
        The transcribed text if the job is successful, otherwise None.
    """
    aai = get_speech_client()
    transcriber = aai.Transcriber()
    start_time = time.time()

    while time.time() - start_time < timeout:
        transcript = transcriber.get(job_id)

        if transcript.status == 'completed':
            return transcript.text
        elif transcript.status == 'error':
            raise RuntimeError(f"Transcription job {job_id} failed with error: {transcript.error}")
        
        time.sleep(interval)

    raise TimeoutError(f"Polling timed out for transcription job {job_id}")

