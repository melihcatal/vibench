import time
from speech_client import get_speech_client
import assemblyai

def poll_transcription_job(job_id: str) -> str:
    """
    Polls a transcription job until completion and returns the transcript text.

    Args:
        job_id: The ID of the transcription job to poll.

    Returns:
        The full transcript text.
    
    Raises:
        Exception: If the transcription job fails.
    """
    transcriber = get_speech_client()
    while True:
        transcript = transcriber.get(job_id)
        if transcript.status == assemblyai.TranscriptStatus.completed:
            return transcript.text
        elif transcript.status == assemblyai.TranscriptStatus.error:
            raise Exception(f"Transcription job {job_id} failed with error: {transcript.error}")
        time.sleep(5)
