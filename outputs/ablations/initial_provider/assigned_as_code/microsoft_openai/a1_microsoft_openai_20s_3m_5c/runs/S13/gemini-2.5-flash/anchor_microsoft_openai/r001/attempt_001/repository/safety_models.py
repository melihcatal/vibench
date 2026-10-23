from typing import List, Dict, Any
from dataclasses import dataclass

@dataclass
class TextModerationRequest:
    text: str

@dataclass
class TextModerationResult:
    category: str
    severity: int

@dataclass
class BatchModerationRequest:
    texts: List[str]

@dataclass
class BatchModerationResult:
    index: int
    text: str
    results: List[TextModerationResult]
    is_unsafe: bool

@dataclass
class RedactionRequest:
    text: str
    categories_to_redact: List[str]

@dataclass
class RedactionResult:
    redacted_text: str
    unsafe_spans: List[Dict[str, Any]]

@dataclass
class ModerationSummaryRequest:
    moderation_results: List[BatchModerationResult]

@dataclass
class ModerationSummaryResponse:
    summary: str

@dataclass
class AppealTranslateRequest:
    text: str
    target_language: str = "en"

@dataclass
class AppealTranslateResponse:
    translated_text: str

@dataclass
class ModerationReasonEmbeddingRequest:
    reason_texts: List[str]

@dataclass
class ModerationReasonEmbeddingResponse:
    embeddings: List[List[float]]

@dataclass
class ReviewerBriefAudioRequest:
    brief_text: str
    
@dataclass
class ReviewerBriefAudioResponse:
    audio_content: bytes
