from speech_client import get_completed_transcription
from speech_models import parse_word_timestamps
from typing import List, Dict

def timestamped_transcript(job_name: str) -> List[Dict[str, str]]:
    """
    Returns word timestamps from a transcription result.
    """
    data = get_completed_transcription(job_name)
    return parse_word_timestamps(data)