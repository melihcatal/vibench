from dataclasses import dataclass
from typing import List, Dict, Optional


@dataclass
class TranscriptionResult:
    """Container for transcription results."""

    transcript_id: str
    text: str
    status: str
    words: List[str]
    segments: List[Dict[str, any]]

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "transcript_id": self.transcript_id,
            "text": self.text,
            "status": self.status,
            "word_count": len(self.words),
            "segment_count": len(self.segments),
        }


@dataclass
class TranscriptionRequest:
    """Container for transcription requests."""

    audio_url: str
    language_code: str = "en"
    speaker_labels: bool = False
    speakers_expected: Optional[int] = None
    word_boost: List[str] = None

    def __post_init__(self):
        if self.word_boost is None:
            self.word_boost = []


def normalize_transcript_text(text: str) -> str:
    """Normalize transcript text."""
    import re

    text = re.sub(r"\s+", " ", text)
    text = text.strip()
    return text


def split_into_segments(text: str, max_segment_length: int = 1000) -> List[str]:
    """Split text into segments for processing."""
    import re

    sentences = re.split(r"(?<=[.!?])\s+", text)

    segments = []
    current_segment = ""

    for sentence in sentences:
        if len(current_segment) + len(sentence) + 1 <= max_segment_length:
            if current_segment:
                current_segment += " " + sentence
            else:
                current_segment = sentence
        else:
            if current_segment:
                segments.append(current_segment)
            current_segment = sentence

    if current_segment:
        segments.append(current_segment)

    return segments
