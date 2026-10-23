from dataclasses import dataclass
from typing import List

@dataclass
class TranscriptChunk:
    """Represents a single chunk of a transcript, final or partial."""
    text: str
    is_final: bool
    timestamp: float

@dataclass
class MeetingTranscript:
    """Represents the full transcript of a meeting composed of chunks."""
    chunks: List[TranscriptChunk]

    def full_text(self) -> str:
        """Joins all final chunks to produce the full transcript text."""
        return " ".join(chunk.text for chunk in self.chunks if chunk.is_final)
