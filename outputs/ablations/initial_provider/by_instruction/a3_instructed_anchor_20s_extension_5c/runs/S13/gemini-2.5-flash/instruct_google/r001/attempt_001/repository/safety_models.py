from typing import List, Dict, Any
from dataclasses import dataclass, field

@dataclass
class ModerationScore:
    category: str
    score: float
    threshold: float = 0.0 # Default threshold

@dataclass
class ModerationResult:
    text: str
    is_flagged: bool
    decision_reason: str
    scores: List[ModerationScore] = field(default_factory=list)
    provider: str = ""

@dataclass
class TextRedactionResult:
    original_text: str
    redacted_text: str
    provider: str = ""

@dataclass
class TranslationRequest:
    text: str
    target_language_code: str
    source_language_code: str = "en"

@dataclass
class TranslationResult:
    original_text: str
    translated_text: str
    source_language: str
    target_language: str
    provider: str = ""

@dataclass
class EmbeddingResult:
    text: str
    embedding: List[float]
    provider: str = ""

@dataclass
class AudioBriefResult:
    text: str
    audio_content: bytes
    provider: str = ""

