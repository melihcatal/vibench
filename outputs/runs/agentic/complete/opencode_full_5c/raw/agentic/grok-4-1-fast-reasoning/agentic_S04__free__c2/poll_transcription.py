import time
import assemblyai as aai
from speech_client import get_client
from speech_models import serialize_transcript


def poll_transcription(job_id: str, poll_interval: int = 30) -> dict:
    client = get_client()
    while True:
        transcript = client.transcripts.get(job_id)
        if transcript.status == aai.TranscriptStatus.completed:
            return serialize_transcript(transcript)
        elif transcript.status == aai.TranscriptStatus.error:
            raise RuntimeError(transcript.error)
        time.sleep(poll_interval)
