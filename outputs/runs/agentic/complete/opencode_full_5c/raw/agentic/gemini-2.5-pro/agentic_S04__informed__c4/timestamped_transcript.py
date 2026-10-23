from typing import List
from speech_client import client
from speech_models import TimestampedWord
from assemblyai import Transcript


def get_timestamped_transcript(job_id: str) -> List[TimestampedWord]:
    """
    Retrieves word-level timestamps from a completed transcription job.
    """
    transcript: Transcript = client.transcripts.get(job_id)
    if transcript.status != "completed":
        raise ValueError(
            f"Transcription job {job_id} is not complete. Status: {transcript.status}"
        )

    if not transcript.words:
        return []

    return [
        {"word": word.text, "start": word.start, "end": word.end}
        for word in transcript.words
    ]
