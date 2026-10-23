import time
from speech_client import SpeechClient


def poll_transcription(job_id: str) -> str:
    """
    Polls an AssemblyAI transcription job and returns the transcript.
    """
    client = SpeechClient()
    while True:
        response = client.get_job(job_id)
        status = response.get("status")
        if status == "completed":
            return response.get("text")
        elif status == "failed":
            raise Exception(
                f"Transcription job {job_id} failed: {response.get('error')}"
            )
        time.sleep(5)
