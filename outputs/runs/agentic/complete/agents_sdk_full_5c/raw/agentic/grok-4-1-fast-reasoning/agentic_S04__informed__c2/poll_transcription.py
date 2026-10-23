import assemblyai as aai
import time
from speech_client import get_api_key

def poll_transcription(job_id: str) -> str:
    aai.settings.api_key = get_api_key()
    transcriber = aai.Transcriber()
    transcript = transcriber.get_transcript(job_id)
    while transcript.status == aai.TranscriptStatus.processing:
        time.sleep(10)
        transcript = transcriber.get_transcript(job_id)
    if transcript.status == aai.TranscriptStatus.error:
        raise RuntimeError(f"Transcription failed: {transcript.error}")
    return transcript.text
