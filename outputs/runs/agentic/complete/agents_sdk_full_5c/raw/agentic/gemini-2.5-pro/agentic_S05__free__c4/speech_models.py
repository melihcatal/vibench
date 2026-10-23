from dataclasses import dataclass
from typing import List

@dataclass
class TranscriptChunk:
    """Represents a single piece of a transcript, final or interim."""
    transcript: str
    is_final: bool
    stability: float
    alternatives: List[str]

def normalize_response_to_chunk(response):
    """
    Normalizes a Google Cloud Speech-to-Text streaming response
    to a TranscriptChunk object.
    """
    if not response.results:
        return None

    result = response.results[0]
    if not result.alternatives:
        return None

    return TranscriptChunk(
        transcript=result.alternatives[0].transcript,
        is_final=result.is_final,
        stability=result.stability,
        alternatives=[alt.transcript for alt in result.alternatives]
    )
