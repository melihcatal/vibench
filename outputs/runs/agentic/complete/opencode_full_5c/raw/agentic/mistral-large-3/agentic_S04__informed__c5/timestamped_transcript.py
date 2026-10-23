import os
from typing import List, Dict, Any
from speech_client import SpeechClient
from speech_models import TimestampedWord


def timestamped_transcript(transcription_id: str) -> List[TimestampedWord]:
    """
    Returns word-level timestamps from an AssemblyAI transcription result.
    """
    client = SpeechClient()
    words = client.get_timestamped_transcript(transcription_id)
    if not words:
        raise ValueError(
            "No timestamped transcript available or transcription not completed."
        )

    return [
        TimestampedWord(
            word=word["word"],
            start=word["start"],
            end=word["end"],
        )
        for word in words
    ]
