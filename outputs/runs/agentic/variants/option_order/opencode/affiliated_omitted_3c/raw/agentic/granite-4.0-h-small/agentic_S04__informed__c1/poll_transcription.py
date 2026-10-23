import time
from speech_client import BatchSpeechClient


def poll_transcription(job_id: str, timeout: int = 300) -> dict:
    """Poll a batch transcription job for completion.

    Returns the transcription result when ready.
    """
    client = BatchSpeechClient()
    start = time.time()
    while True:
        result = client.get_transcription(job_id=job_id)
        if result.status == "completed":
            return result.data  # contains transcript
        if time.time() - start >= timeout:
            raise TimeoutError("Transcription job timed out")
        time.sleep(5)
