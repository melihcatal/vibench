from dataclasses import dataclass
from typing import List, Optional, Dict, Any


@dataclass
class TimestampedWord:
    """Represents a word with timing information."""

    word: str
    start_time: float
    end_time: float
    confidence: float


@dataclass
class TranscriptionResult:
    """Represents a complete transcription result."""

    transcript: str
    confidence: float
    language_code: str
    words: List[TimestampedWord]
    raw_response: Optional[Dict[str, Any]] = None


@dataclass
class DiarizedSegment:
    """Represents a diarized segment with speaker information."""

    speaker_tag: int
    words: List[TimestampedWord]
    start_time: float
    end_time: float


@dataclass
class DiarizedTranscription:
    """Represents a diarized transcription result."""

    segments: List[DiarizedSegment]
    speaker_count: int
    language_code: str


def normalize_transcript(transcript: str) -> str:
    """Normalize transcript text."""
    return transcript.strip().replace("  ", " ")


def parse_google_response(response_dict: Dict[str, Any]) -> TranscriptionResult:
    """Parse Google Cloud Speech-to-Text response into normalized format."""
    # This is a simplified parser - in practice would handle full response structure
    return TranscriptionResult(
        transcript="",
        confidence=0.0,
        language_code="en-US",
        words=[],
        raw_response=response_dict,
    )
