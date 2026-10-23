from assemblyai import Client, TranscriptionStatus
import time
from speech_client import get_assemblyai_api_key
from speech_models import normalize_transcript, TranscriptResult


def poll_transcription(job_id: str) -> TranscriptResult:
    api_key = get_assemblyai_api_key()
    client = Client(api_key=api_key)
    transcript = client.transcripts.get(job_id)
    while transcript.status != TranscriptionStatus.completed:
        if transcript.status == TranscriptionStatus.error:
            raise ValueError(
                f"Transcription error: {getattr(transcript, 'error', 'Unknown error')}"
            )
        time.sleep(30)
        transcript = client.transcripts.get(job_id)
    return normalize_transcript(transcript)
