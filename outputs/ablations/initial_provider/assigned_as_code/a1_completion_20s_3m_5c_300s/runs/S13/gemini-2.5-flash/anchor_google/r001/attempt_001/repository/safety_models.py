from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class ModerationRequest:
    text: str
    language_code: str = "en"
    attributes: List[str] = field(default_factory=lambda: ["TOXICITY", "SEVERE_TOXICITY", "IDENTITY_ATTACK", "INSULT", "PROFANITY", "THREAT", "SEXUALLY_EXPLICIT", "FLIRTATION"])

@dataclass
class ModerationResult:
    category: str
    score: float
    decision: str = "pending"

@dataclass
class BatchModerationRequest:
    texts: List[str]
    language_code: str = "en"

@dataclass
class BatchModerationResult:
    original_text: str
    results: List[ModerationResult]

@dataclass
class RedactionRequest:
    text: str
    threshold: float = 0.7
    category: str = "TOXICITY"

@dataclass
class RedactionResult:
    original_text: str
    redacted_text: str
    detected_spans: List[Dict[str, Any]]

@dataclass
class ModerationSummaryRequest:
    moderation_decisions: List[Dict[str, Any]]

@dataclass
class ModerationSummaryResult:
    summary: str

@dataclass
class TranslationRequest:
    text: str
    target_language: str
    source_language: Optional[str] = None

@dataclass
class TranslationResult:
    translated_text: str

@dataclass
class EmbeddingRequest:
    text: str

@dataclass
class EmbeddingResult:
    embedding: List[float]

@dataclass
class ReviewerBriefAudioRequest:
    text: str
    voice_name: str = "en-US-Neural2-A"
    audio_encoding: str = "MP3"
