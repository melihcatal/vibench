from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field


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


class OpenAIModerationResponse(BaseModel):
    id: str
    model: str
    results: List[ModerationResult]


class RedactionRequest(BaseModel):
    text: str


class Redaction(BaseModel):
    text: str
    start: int
    end: int
    label: str


class RedactionResponse(BaseModel):
    redacted_text: str
    redactions: List[Redaction]


class ModerationDecision(BaseModel):
    text: str
    is_safe: bool
    violations: List[str]
    scores: Optional[Dict[str, float]] = None


class TranslationRequest(BaseModel):
    text: str
    target_language: str


class TranslationResponse(BaseModel):
    translated_text: str
    detected_source_language: str


class EmbeddingRequest(BaseModel):
    texts: List[str]


class EmbeddingResponse(BaseModel):
    embeddings: List[List[float]]


class AudioRequest(BaseModel):
    text: str
    voice_id: str


class SummaryRequest(BaseModel):
    decisions: List[ModerationDecision]
