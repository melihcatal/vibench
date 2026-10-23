from typing import Dict, List, Optional, Union
from pydantic import BaseModel


class ModerationRequest(BaseModel):
    text: str
    language: Optional[str] = "en"


class AttributeScore(BaseModel):
    summary_score: float


class ModerationResponse(BaseModel):
    attribute_scores: Dict[str, AttributeScore]
    raw_response: Dict


class RedactionResult(BaseModel):
    original_text: str
    redacted_text: str
    unsafe_spans: List[Dict[str, Union[int, int, str]]]


class BatchModerationResult(BaseModel):
    results: List[ModerationResponse]
    is_batch: bool = True
