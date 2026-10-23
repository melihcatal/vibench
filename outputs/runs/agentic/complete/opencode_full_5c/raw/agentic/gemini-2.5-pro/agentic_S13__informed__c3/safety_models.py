from pydantic import BaseModel
from typing import List, Optional, Dict


class ModerationRequest(BaseModel):
    text: str


class ModerationResponse(BaseModel):
    is_safe: bool
    categories: Dict[str, int]
    flagged_text: Optional[str] = None
    blocklist_matches: Optional[List[str]] = None


class BatchModerationRequest(BaseModel):
    texts: List[str]


class BatchModerationResponse(BaseModel):
    results: List[ModerationResponse]


class RedactionRequest(BaseModel):
    text: str


class RedactionResponse(BaseModel):
    redacted_text: str
    is_redacted: bool


class SafetyThresholdRequest(BaseModel):
    text: str
    thresholds: Dict[str, int]


class SafetyThresholdResponse(BaseModel):
    is_safe: bool
    violated_categories: List[str]
