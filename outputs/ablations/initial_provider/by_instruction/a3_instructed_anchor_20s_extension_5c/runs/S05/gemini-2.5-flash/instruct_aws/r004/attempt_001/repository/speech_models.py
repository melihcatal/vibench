import dataclasses
from typing import List, Optional

@dataclasses.dataclass
class TranscriptResult:
    text: str
    is_partial: bool
    confidence: Optional[float] = None

@dataclasses.dataclass
class SpeechRecognitionRequest:
    audio_chunk: bytes
    sample_rate_hertz: int
    language_code: str
    encoding: str = "LINEAR16"

@dataclasses.dataclass
class TranslationResult:
    translated_text: str
    source_language: str
    target_language: str

@dataclasses.dataclass
class SafetyCheckResult:
    is_unsafe: bool
    categories: List[str]
    scores: dict

@dataclasses.dataclass
class MeetingSummaryResult:
    summary: str

@dataclasses.dataclass
class CaptionEmbeddingResult:
    embedding: List[float]
