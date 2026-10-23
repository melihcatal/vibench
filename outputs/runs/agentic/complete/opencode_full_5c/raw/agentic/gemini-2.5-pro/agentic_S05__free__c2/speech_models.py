from dataclasses import dataclass


@dataclass
class TranscriptSegment:
    """Represents a segment of a transcript."""

    text: str
    is_final: bool
    stability: float
    language_code: str = "en-US"
