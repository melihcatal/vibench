from pydantic import BaseModel
from typing import List, Optional


class TextModerationRequest(BaseModel):
    text: str


class TextModerationResult(BaseModel):
    category: str
    severity: int
    moderated: bool


class TextModerationResponse(BaseModel):
    id: Optional[str]
    categories_analysis: List[TextModerationResult]


class BatchModerationRequest(BaseModel):
    texts: List[str]


class BatchModerationResponse(BaseModel):
    results: List[List[TextModerationResult]]


class RedactionRequest(BaseModel):
    text: str


class RedactionResponse(BaseModel):
    redacted_text: str


class ThresholdConfig(BaseModel):
    category: str
    threshold: int


class SafetyThresholdRequest(BaseModel):
    text: str
    thresholds: List[ThresholdConfig]


class SafetyThresholdResponse(BaseModel):
    text: str
    allowed: bool
    reasons: List[str]


class ModerationDecision(BaseModel):
    text: str
    decision: str
    reason: str


class ModerationSummaryRequest(BaseModel):
    decisions: List[ModerationDecision]


class ModerationSummaryResponse(BaseModel):
    summary: str


class AppealTranslateRequest(BaseModel):
    text: str
    target_lang: str


class AppealTranslateResponse(BaseModel):
    translated_text: str


class ModerationReasonEmbeddingRequest(BaseModel):
    reason: str


class ModerationReasonEmbeddingResponse(BaseModel):
    embedding: List[float]


class ReviewerBriefAudioRequest(BaseModel):
    brief_text: str


class ReviewerBriefAudioResponse(BaseModel):
    audio_content: bytes
