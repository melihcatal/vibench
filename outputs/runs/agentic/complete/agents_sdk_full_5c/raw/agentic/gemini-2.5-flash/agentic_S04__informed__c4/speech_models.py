from dataclasses import dataclass, field
from typing import Optional

@dataclass
class TranscriptionOptions:
    """Defines common transcription options for batch speech-to-text."""
    speaker_labels: bool = False
    auto_chapters: bool = False
    sentiment_analysis: bool = False
    iab_categories: bool = False
    word_boost: Optional[list[str]] = field(default_factory=list)
    boost_param: Optional[str] = None # e.g., high

@dataclass
class TranscriptResult:
    """Represents a simplified transcription result."""
    job_id: str
    text: Optional[str] = None
    status: str = "submitted"
    error: Optional[str] = None
    # Add more fields as needed, e.g., for timestamps or diarization


@dataclass
class WordTimestamp:
    """Represents a single word with its timestamp and speaker information."""
    word: str
    start: int # milliseconds
    end: int # milliseconds
    speaker: Optional[str] = None
