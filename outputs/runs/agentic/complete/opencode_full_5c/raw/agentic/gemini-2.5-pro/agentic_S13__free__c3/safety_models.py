from typing import List, Dict, Optional
from pydantic import BaseModel, Field


class ModerationRequest(BaseModel):
    text: str


class ModerationResponse(BaseModel):
    flagged: bool
    categories: Dict[str, bool]
    category_scores: Dict[str, float]


class BatchModerationRequest(BaseModel):
    texts: List[str]


class BatchModerationResponse(BaseModel):
    results: List[ModerationResponse]


class RedactUnsafeRequest(BaseModel):
    text: str


class RedactedText(BaseModel):
    text: str
    redacted_spans: List[tuple[int, int]]


class RedactUnsafeResponse(BaseModel):
    redacted_text: RedactedText


class SafetyThresholdRequest(BaseModel):
    category_scores: Dict[str, float]
    thresholds: Dict[str, float]


class SafetyThresholdResponse(BaseModel):
    allowed: bool
    violations: Dict[str, float]


class ModerationSummaryRequest(BaseModel):
    decisions: List[ModerationResponse]


class ModerationSummaryResponse(BaseModel):
    summary: str


class AppealTranslateRequest(BaseModel):
    text: str
    target_language: str = "en"


class AppealTranslateResponse(BaseModel):
    translated_text: str


class ModerationReasonEmbeddingRequest(BaseModel):
    reasons: List[str]


class ModerationReasonEmbeddingResponse(BaseModel):
    embeddings: List[List[float]]


class ReviewerBriefAudioRequest(BaseModel):
    brief_text: str


class ReviewerBriefAudioResponse(BaseModel):
    audio_content: bytes
