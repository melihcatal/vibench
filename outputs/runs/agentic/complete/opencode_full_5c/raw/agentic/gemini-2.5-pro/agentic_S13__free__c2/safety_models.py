from pydantic import BaseModel, Field
from typing import List, Dict


class ModerationCategoryScores(BaseModel):
    hate: float
    hate_threatening: float = Field(..., alias="hate/threatening")
    harassment: float
    harassment_threatening: float = Field(..., alias="harassment/threatening")
    self_harm: float
    self_harm_intent: float = Field(..., alias="self-harm/intent")
    self_harm_instructions: float = Field(..., alias="self-harm/instructions")
    sexual: float
    sexual_minors: float = Field(..., alias="sexual/minors")
    violence: float
    violence_graphic: float = Field(..., alias="violence/graphic")


class ModerationResult(BaseModel):
    flagged: bool
    categories: Dict[str, bool]
    category_scores: ModerationCategoryScores


class ModerationResponse(BaseModel):
    id: str
    model: str
    results: List[ModerationResult]


class RedactionRequest(BaseModel):
    text: str
    language_code: str = "en"


class RedactionResponse(BaseModel):
    redacted_text: str
    toxic_spans: List[Dict[str, float]]


class Thresholds(BaseModel):
    hate: float = 0.8
    sexual: float = 0.6
    violence: float = 0.7
    harassment: float = 0.7
    self_harm: float = 0.5
