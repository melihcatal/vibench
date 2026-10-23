from typing import List, Dict
from speech_client import get_assemblyai_client
from speech_models import TimestampedWord

def timestamped_transcript(job_id: str) -> List[TimestampedWord]:
    """
    Retrieve word-level timestamps for a completed AssemblyAI transcription job.
    Returns a list of words with their start and end timestamps.
    """
    client = get_assemblyai_client()
    transcript = client.transcripts.get(job_id)
    if transcript.status != "completed":
        raise ValueError(f"Transcription job not completed. Status: {transcript.status}")

    words = transcript.words
    if not words:
        raise ValueError("No word-level timestamp data available.")

    timestamped_words = []
    for word in words:
        timestamped_words.append(
            TimestampedWord(
                word=word.text,
                start=word.start,
                end=word.end
            )
        )
    return timestamped_words