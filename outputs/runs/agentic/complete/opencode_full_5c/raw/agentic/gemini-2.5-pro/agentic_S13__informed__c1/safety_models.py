from typing import List, Dict, Optional
from pydantic import BaseModel


class ModerationRequest(BaseModel):
    text: str


class BatchModerationRequest(BaseModel):
    texts: List[str]


class CategoryScore(BaseModel):
    category: str
    severity: int


class ModerationResponse(BaseModel):
    text: str
    scores: List[CategoryScore]


class RedactionRequest(BaseModel):
    text: str
    blocklist_name: str


class RedactedSpan(BaseModel):
    text: str
    offset: int
    length: int


class RedactionResponse(BaseModel):
    redacted_text: str
    flagged_spans: List[RedactedSpan]


class ThresholdRequest(BaseModel):
    scores: List[CategoryScore]
    thresholds: Dict[str, int]  # Category -> Severity Threshold


class ThresholdDecision(BaseModel):
    allow: bool
    violated_categories: List[str]
