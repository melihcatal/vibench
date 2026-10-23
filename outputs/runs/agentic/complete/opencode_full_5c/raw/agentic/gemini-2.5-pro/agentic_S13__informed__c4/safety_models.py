from typing import List, Optional, Dict
from pydantic import BaseModel


class SafetyCategory(BaseModel):
    category: str
    severity: int


class ModerationResponse(BaseModel):
    hate: Optional[SafetyCategory] = None
    self_harm: Optional[SafetyCategory] = None
    sexual: Optional[SafetyCategory] = None
    violence: Optional[SafetyCategory] = None
    profanity: Optional[SafetyCategory] = None
    success: bool = True


class BatchModerationResponse(BaseModel):
    results: List[ModerationResponse]


class RedactionResult(BaseModel):
    redacted_text: str
    blocklist_matches: List[Dict]


class ThresholdDecision(BaseModel):
    is_allowed: bool
    breached_categories: List[SafetyCategory]
