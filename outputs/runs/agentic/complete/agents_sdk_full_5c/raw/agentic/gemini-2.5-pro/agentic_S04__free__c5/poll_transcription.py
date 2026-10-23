import time
from assemblyai import TranscriptStatus
from speech_client import get_transcript_by_id

def poll_for_transcript(job_id: str) -> str:
    """
    Polls a transcription job until it is completed and returns the transcript text.

    Args:
        job_id: The ID of the transcription job to poll.

    Returns:
        The full text of the transcript.
    """
    transcript = get_transcript_by_id(job_id)

    while transcript.status not in [TranscriptStatus.completed, TranscriptStatus.error]:
        time.sleep(5)
        transcript = transcript.get()

    if transcript.status == TranscriptStatus.error:
        raise Exception(f"Transcription failed: {transcript.error}")

    return transcript.text
