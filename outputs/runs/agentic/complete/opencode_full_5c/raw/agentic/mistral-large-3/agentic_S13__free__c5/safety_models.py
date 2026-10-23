from typing import Dict, Any, List, Optional
from pydantic import BaseModel


class ModerationScore(BaseModel):
    category: str
    score: float
    threshold: Optional[float] = None


class ModerationDecision(BaseModel):
    allow: bool
    violations: List[ModerationScore]
    text: Optional[str] = None


class UnsafeSpan(BaseModel):
    text: str
    offset: int
    length: int
    entity_type: str
    sentiment_score: float


class RedactionResult(BaseModel):
    original_text: str
    redacted_text: str
    unsafe_spans: List[UnsafeSpan]


def normalize_moderation_response(response: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalizes Google Cloud Content Moderation API response into a consistent format.
    """
    attribute_scores = response.get("attributeScores", {})
    normalized = {
        "scores": {
            category: scores["summaryScore"]["value"]
            for category, scores in attribute_scores.items()
        }
    }
    return normalized
