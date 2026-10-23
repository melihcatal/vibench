import os
import assemblyai as aai
import time
from speech_client import get_speech_client
from speech_models import parse_transcript


def poll_transcription(job_id: str, poll_interval: int = 10) -> dict:
    api_key = os.getenv("ASSEMBLYAI_API_KEY")
    client = get_speech_client(api_key)
    transcript = client.transcripts.get(job_id)
    while transcript.status in [
        aai.TranscriptStatus.queued,
        aai.TranscriptStatus.processing,
    ]:
        time.sleep(poll_interval)
        transcript = client.transcripts.get(job_id)
    if transcript.status == aai.TranscriptStatus.error:
        raise RuntimeError(
            f"Transcription error: {getattr(transcript, 'error', 'Unknown error')}"
        )
    return parse_transcript(transcript)
