import time
from speech_client import client
from speech_models import TranscriptionResult
from assemblyai import Transcript, TranscriptStatus


def poll_transcription(job_id: str) -> str:
    """
    Polls a transcription job until it is completed and returns the transcript text.
    """
    while True:
        transcript: Transcript = client.transcripts.get(job_id)
        if transcript.status == TranscriptStatus.completed:
            return transcript.text
        elif transcript.status == TranscriptStatus.error:
            return f"Transcription failed: {transcript.error}"
        time.sleep(5)
