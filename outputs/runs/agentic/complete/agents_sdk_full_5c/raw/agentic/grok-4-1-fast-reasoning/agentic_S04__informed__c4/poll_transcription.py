import time
import assemblyai as aai
from speech_client import get_client

def poll_transcription(job_id: str) -> str:
    client = get_client()
    transcript = client.transcripts.get(job_id)
    while transcript.status not in [aai.TranscriptStatus.completed, aai.TranscriptStatus.error]:
        time.sleep(10)
        transcript = client.transcripts.get(job_id)
    if transcript.status == aai.TranscriptStatus.error:
        raise ValueError(f"Transcription failed: {transcript.error}")
    return transcript.text