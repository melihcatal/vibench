import dataclasses
import collections
from typing import List, Optional

@dataclasses.dataclass
class SpeechRecognitionChunk:
    text: str
    is_final: bool

@dataclasses.dataclass
class TranscriptResult:
    text: str
    language: Optional[str] = None

@dataclasses.dataclass
class ModerationResult:
    flagged: bool
    categories: dict

@dataclasses.dataclass
class TranslationResult:
    translated_text: str
    detected_language: Optional[str] = None

@dataclasses.dataclass
class EmbeddingResult:
    embedding: List[float]

@dataclasses.dataclass
class SummaryResult:
    summary: str
