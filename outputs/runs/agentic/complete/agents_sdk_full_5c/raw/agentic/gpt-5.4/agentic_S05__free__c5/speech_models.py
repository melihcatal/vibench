from dataclasses import dataclass
from typing import Iterable, List, Optional


@dataclass(slots=True)
class TranscriptChunk:
    text: str
    is_final: bool = False
    stability: Optional[float] = None
    language_code: Optional[str] = None


@dataclass(slots=True)
class NormalizedCaption:
    source_text: str
    normalized_text: str
    is_final: bool = False


@dataclass(slots=True)
class SafetyCheckResult:
    text: str
    blocked: bool
    reason: Optional[str] = None


@dataclass(slots=True)
class SummaryResult:
    summary: str
    source_chunk_count: int


@dataclass(slots=True)
class EmbeddingResult:
    text: str
    vector: List[float]
    model: str



def normalize_transcript_text(text: str) -> str:
    return " ".join(text.strip().split())



def merge_caption_text(chunks: Iterable[TranscriptChunk]) -> str:
    return " ".join(normalize_transcript_text(chunk.text) for chunk in chunks if chunk.text).strip()
