from dataclasses import dataclass
from typing import Optional


@dataclass
class TranscriptChunk:
    text: str
    is_final: bool
    channel: Optional[str] = None


def normalize_transcript(text: str) -> str:
    return text.strip()
