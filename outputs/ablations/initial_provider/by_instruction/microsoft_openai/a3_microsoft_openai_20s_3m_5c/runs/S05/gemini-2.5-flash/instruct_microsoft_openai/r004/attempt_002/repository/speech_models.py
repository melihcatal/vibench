from dataclasses import dataclass

@dataclass
class AudioChunk:
    data: bytes
    timestamp: float | None = None
    sequence_number: int | None = None

@dataclass
class TranscriptResult:
    text: str
    is_partial: bool
    language: str | None = None
    confidence: float | None = None

# Placeholder for normalization helpers if needed later
def normalize_transcript(transcript: str) -> str:
    return transcript.lower().strip()
