import time
import assemblyai as aai
from speech_client import configure_assemblyai

def poll_transcription(job_id):
    configure_assemblyai()
    transcriber = aai.Transcriber()
    transcript = transcriber.get_transcript(job_id)
    while transcript.status not in [aai.TranscriptStatus.completed, aai.TranscriptStatus.error]:
        time.sleep(5)
        transcript = transcriber.get_transcript(job_id)
    if transcript.status == aai.TranscriptStatus.error:
        raise ValueError(f"Transcription failed: {transcript.error}")
    return transcript.text