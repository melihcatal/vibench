from typing import List, Dict
from speech_client import get_assemblyai_client
from speech_models import WordTimestamp


def timestamped_transcript(job_id: str) -> List[WordTimestamp]:
    """
    Retrieve word-level timestamps from an AssemblyAI transcription job.
    Returns a list of words with their start and end timestamps.
    """
    client = get_assemblyai_client()
    transcript = client.transcripts.get(job_id)
    if not transcript.words:
        raise ValueError(f"No word timestamps found for job {job_id}")
    
    return [
        WordTimestamp(
            word=word.text,
            start=word.start,
            end=word.end
        )
        for word in transcript.words
    ]