from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class TranslationRequest:
    content: str
    target_language: str
    source_language: Optional[str] = None

@dataclass
class BatchTranslationRequest:
    content: List[str]
    target_language: str
    source_language: Optional[str] = None

@dataclass
class TranslationResponse:
    translated_text: str
    detected_source_language: Optional[str] = None

@dataclass
class BatchTranslationResponse:
    translations: List[TranslationResponse]

@dataclass
class QualitySummary:
    score: float
    issues: List[str]
    summary_text: str

@dataclass
class UnsafeContentResult:
    scores: Dict[str, float]
    is_unsafe: bool

@dataclass
class EmbeddingVector:
    vector: List[float]
    model: str
