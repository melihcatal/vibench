from typing import List
from speech_client import get_aai_transcript
from speech_models import WordTimestamp


def get_timestamped_transcript(job_id: str) -> List[WordTimestamp]:
    """Returns word or segment timestamps from a transcription result using AssemblyAI."""
    result = get_aai_transcript(job_id)
    if result.words is None:
        raise ValueError(
            "Word timestamp information not available. Ensure word_timestamps was enabled during submission."
        )
    return result.words
