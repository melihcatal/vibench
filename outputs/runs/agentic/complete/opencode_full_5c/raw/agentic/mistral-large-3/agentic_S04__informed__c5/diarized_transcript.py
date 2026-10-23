import os
from typing import List, Dict, Any
from speech_client import SpeechClient
from speech_models import DiarizedUtterance


def diarized_transcript(transcription_id: str) -> List[DiarizedUtterance]:
    """
    Requests speaker diarization for a recorded meeting using AssemblyAI.
    Returns a list of utterances with speaker labels.
    """
    client = SpeechClient()
    utterances = client.get_diarized_transcript(transcription_id)
    if not utterances:
        raise ValueError(
            "No diarized transcript available or transcription not completed."
        )

    return [
        DiarizedUtterance(
            speaker=utterance["speaker"],
            text=utterance["text"],
            start=utterance["start"],
            end=utterance["end"],
        )
        for utterance in utterances
    ]
