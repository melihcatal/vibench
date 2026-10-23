from typing import Dict, List, Union
from pydantic import BaseModel


class ModerationResult(BaseModel):
    """Standardized moderation result model."""

    is_safe: bool
    score: float
    categories: Dict[str, float]
    flagged_reason: str = ""


class RedactionResult(BaseModel):
    """Standardized redaction result model."""

    redacted_text: str
    unsafe_spans: List[Dict[str, Union[int, int, str, float]]]
    is_safe: bool


class BatchModerationResult(BaseModel):
    """Standardized batch moderation result model."""

    results: List[ModerationResult]
    batch_id: str = ""


class SafetyThresholdConfig(BaseModel):
    """Configuration for safety thresholds."""

    thresholds: Dict[str, float]
    default_threshold: float = 0.75


class ModerationSummary(BaseModel):
    """Summary of moderation decisions."""

    total_messages: int
    flagged_messages: int
    flagged_categories: Dict[str, int]
    safety_score: float


class AppealTranslation(BaseModel):
    """Translated appeal text for review."""

    original_text: str
    translated_text: str
    source_language: str
    target_language: str


class ModerationRationaleEmbedding(BaseModel):
    """Embedding for moderation rationale."""

    rationale: str
    embedding: List[float]
    case_id: str = ""


class ReviewerBriefAudio(BaseModel):
    """Generated audio brief for moderation reviewers."""

    audio_content: bytes
    text_content: str
    duration_seconds: float
