from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any

@dataclass
class TranscriptionRequest:
    audio_url: str
    speaker_labels: bool = False
    word_timestamps: bool = False

@dataclass
class WordTimestamp:
    word: str
    start: int
    end: int

@dataclass
class TranscriptionResult:
    text: Optional[str]
    status: str

@dataclass
class DiarizationResult:
    speakers: Optional[List[Dict[str, str]]]
    status: str

@dataclass
class TimestampedTranscriptResult:
    words: Optional[List[WordTimestamp]]
    status: str

@dataclass
class TranslatedSegment:
    original_text: str
    translated_text: str
    source_language: str
    target_language: str

@dataclass
class ModerationResult:
    text: str
    is_safe: bool
    categories: Dict[str, Any]

@dataclass
class SummaryResult:
    original_text: str
    summary: str

@dataclass
class EmbeddingResult:
    text_segment: str
    embedding: List[float]
