from dataclasses import dataclass, field
from typing import Dict, List

@dataclass
class ModerationRequest:
    text: str
    message_id: str = ""
    user_id: str = ""

@dataclass
class ModerationResponse:
    flagged: bool
    categories: Dict[str, bool] = field(default_factory=dict)
    category_scores: Dict[str, float] = field(default_factory=dict)
    redacted_text: str = ""

@dataclass
class BatchModerationRequest:
    texts: List[ModerationRequest]

@dataclass
class BatchModerationResponse:
    results: List[ModerationResponse]

@dataclass
class RedactionRequest:
    text: str

@dataclass
class RedactionResponse:
    redacted_text: str
    flagged_categories: Dict[str, bool] = field(default_factory=dict)

@dataclass
class ThresholdConfig:
    category: str
    threshold: float
    action: str # e.g., "allow", "flag", "block"

@dataclass
class TextDecision:
    text: str
    decision: str # e.g., "allow", "flag", "block"
    reasons: List[str] = field(default_factory=list)

@dataclass
class ModerationSummaryRequest:
    decisions: List[TextDecision]

@dataclass
class ModerationSummaryResponse:
    summary: str

@dataclass
class AppealRequest:
    original_text: str
    moderation_decision: TextDecision
    appeal_reason: str

@dataclass
class TranslatedAppeal:
    translated_text: str
    source_language: str
    target_language: str

@dataclass
class EmbeddingRequest:
    texts: List[str]

@dataclass
class EmbeddingResponse:
    embeddings: List[List[float]]

@dataclass
class ReviewerBriefRequest:
    summary_text: str

@dataclass
class ReviewerBriefAudioResponse:
    audio_content: bytes
    content_type: str
