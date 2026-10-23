import time
from speech_client import get_speech_client
from speech_models import TranscriptionResult


def poll_transcription_job(job_id: str) -> TranscriptionResult:
    """
    Polls a transcription job from AssemblyAI and returns the transcript text.
    """
    client = get_speech_client()
    while True:
        transcript = client.transcripts.get(transcript_id=job_id)
        if transcript.status == "completed":
            return TranscriptionResult(transcript_text=transcript.text)
        elif transcript.status == "error":
            raise Exception(f"Transcription failed: {transcript.error}")
        time.sleep(5)
