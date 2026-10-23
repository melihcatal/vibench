from typing import List, Optional
from pydantic import BaseModel

class TranscriptSegment(BaseModel):
    """
    Represents a segment of a transcript with timestamps.
    """
    text: str
    start: int
    end: int

class DiarizedUtterance(BaseModel):
    """
    Represents a single utterance in a diarized transcript.
    """
    speaker: str
    text: str
    start: int
    end: int
