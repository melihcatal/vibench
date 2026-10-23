import time
from speech_client import get_speech_client
from assemblyai import TranscriptionStatus


def poll_transcription_job(job_id: str) -> str:
    """
    Polls a transcription job until it's complete and returns the text.
    """
    client = get_speech_client()
    while True:
        transcript = client.transcripts.get(job_id)
        if transcript.status == TranscriptionStatus.completed:
            return transcript.text
        elif transcript.status == TranscriptionStatus.error:
            raise RuntimeError(f"Transcription failed: {transcript.error}")
        time.sleep(5)
