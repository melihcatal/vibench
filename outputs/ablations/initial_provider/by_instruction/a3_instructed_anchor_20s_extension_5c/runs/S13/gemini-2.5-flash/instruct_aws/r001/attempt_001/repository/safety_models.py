import dataclasses
from typing import List, Optional

@dataclasses.dataclass
class TextModerationRequest:
    text: str

@dataclasses.dataclass
class TextModerationResponse:
    is_unsafe: bool
    reasons: List[str]
    scores: dict

@dataclasses.dataclass
class BatchModerationRequest:
    texts: List[str]

@dataclasses.dataclass
class BatchModerationResponse:
    results: List[TextModerationResponse]

@dataclasses.dataclass
class RedactionRequest:
    text: str
    unsafe_spans: List[dict]

@dataclasses.dataclass
class RedactionResponse:
    redacted_text: str

@dataclasses.dataclass
class ThresholdConfig:
    category: str
    threshold: float

@dataclasses.dataclass
class ModerationSummaryRequest:
    decisions: List[TextModerationResponse]
    original_texts: List[str]

@dataclasses.dataclass
class ModerationSummaryResponse:
    summary: str

@dataclasses.dataclass
class AppealTranslateRequest:
    text: str
    target_language: str

@dataclasses.dataclass
class AppealTranslateResponse:
    translated_text: str

@dataclasses.dataclass
class ModerationReasonEmbeddingRequest:
    reasons: List[str]

@dataclasses.dataclass
class ModerationReasonEmbeddingResponse:
    embeddings: List[List[float]]

@dataclasses.dataclass
class ReviewerBriefAudioRequest:
    text: str

@dataclasses.dataclass
class ReviewerBriefAudioResponse:
    audio_content: bytes
