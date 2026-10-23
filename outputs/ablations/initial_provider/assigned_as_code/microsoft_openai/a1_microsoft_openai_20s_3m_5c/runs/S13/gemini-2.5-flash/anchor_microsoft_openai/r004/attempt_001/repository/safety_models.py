from typing import List, Literal, Optional
from pydantic import BaseModel, Field


class TextModerationRequest(BaseModel):
    text: str


class TextModerationResponse(BaseModel):
    toxicity: float = Field(..., ge=0.0, le=1.0)


class BatchModerationRequest(BaseModel):
    texts: List[str]


class MessageDecision(BaseModel):
    text: str
    decision: Literal['allow', 'flag', 'block']
    reasons: List[str] = []


class BatchModerationResponse(BaseModel):
    decisions: List[MessageDecision]


class RedactRequest(BaseModel):
    text: str


class RedactResponse(BaseModel):
    redacted_text: str
    is_unsafe: bool


class ContentCategory(BaseModel):
    category: str
    severity: int


class ModerationResult(BaseModel):
    text: str
    categories: List[ContentCategory]


class ThresholdConfig(BaseModel):
    category: str
    threshold: int
    action: Literal['flag', 'block']


class SafetyThresholdRequest(BaseModel):
    moderation_result: ModerationResult
    threshold_configs: List[ThresholdConfig]


class ModerationSummaryRequest(BaseModel):
    decisions: List[MessageDecision]


class ModerationSummaryResponse(BaseModel):
    summary: str


class AppealTranslateRequest(BaseModel):
    appeal_text: str
    target_language: str = "en"


class AppealTranslateResponse(BaseModel):
    translated_text: str


class ModerationReasonEmbeddingRequest(BaseModel):
    reasons: List[str]


class ModerationReasonEmbeddingResponse(BaseModel):
    embeddings: List[List[float]]


class ReviewerBriefAudioRequest(BaseModel):
    summary: str
    language_code: str = "en-US"
    voice_name: str = "en-US-Standard-A"


class ReviewerBriefAudioResponse(BaseModel):
    audio_content: str
