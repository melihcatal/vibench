import time
from speech_client import get_speech_client
from assemblyai import TranscriptStatus


def poll_transcription(
    job_id: str, poll_interval: int = 10, timeout: int = 600
) -> dict:
    client = get_speech_client()
    start_time = time.time()
    while time.time() - start_time < timeout:
        transcript = client.transcripts.retrieve(job_id)
        if transcript.status == TranscriptStatus.completed:
            return transcript.json_response
        if transcript.status == TranscriptStatus.error:
            raise ValueError(f"Transcription error: {transcript.error}")
        time.sleep(poll_interval)
    raise TimeoutError("Transcription polling timed out")
