import time
import assemblyai as aai
from speech_client import get_speech_client
from speech_models import get_transcript_text

def poll_transcription(job_id: str) -> str:
    client = get_speech_client()
    transcript = client.transcripts.get(job_id)
    while transcript.status not in [aai.TranscriptStatus.completed, aai.TranscriptStatus.error]:
        time.sleep(5)
        transcript = client.transcripts.get(job_id)
    if transcript.status == aai.TranscriptStatus.error:
        raise ValueError(f'Transcription error: {getattr(transcript, "error", "Unknown error")}')
    return get_transcript_text(transcript)