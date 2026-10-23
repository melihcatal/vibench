from dataclasses import dataclass, field
from typing import Optional, List, AsyncIterator

@dataclass
class AudioChunk:
    content: bytes
    sample_rate_hertz: int

@dataclass
class TranscriptResult:
    transcript: str
    is_final: bool
    confidence: float = 0.0
    language_code: Optional[str] = None

@dataclass
class TranslatedCaption:
    original_text: str
    translated_text: str
    source_language: str
    target_language: str

@dataclass
class SafetyDetectionResult:
    text: str
    categories: List[str]
    scores: List[float]
    is_safe: bool

@dataclass
class MeetingSummaryResult:
    summary_text: str
    source_text: str

@dataclass
class CaptionEmbeddingResult:
    text: str
    embedding: List[float]
