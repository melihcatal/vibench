from typing import List, Optional, Dict
from pydantic import BaseModel, Field


class SafetyCategory(BaseModel):
    category: str
    score: float
    threshold: Optional[float] = None


class SafetyDecision(BaseModel):
    text: str
    is_safe: bool
    reason: Optional[str] = None
    categories: List[SafetyCategory] = Field(default_factory=list)


class ModerationResponse(BaseModel):
    decisions: List[SafetyDecision]

class ModerationSummary(BaseModel):
    overall_decision: str
    summary_text: str
    key_themes: List[str]
    confidence: float
