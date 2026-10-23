from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field

class ModerationRequest(BaseModel):
    text: str
    user_id: Optional[str] = None

class ModerationCategoryScores(BaseModel):
    hate: float
    hate_threatening: float
    harassment: float
    harassment_threatening: float
    self_harm: float
    self_harm_intent: float
    self_harm_instructions: float
    sexual: float
    sexual_minors: float
    violence: float
    violence_graphic: float

class ModerationResult(BaseModel):
    flagged: bool
    categories: Dict[str, bool]
    scores: ModerationCategoryScores

class BatchModerationRequest(BaseModel):
    texts: List[str]

class RedactionRequest(BaseModel):
    text: str

class RedactedText(BaseModel):
    original_text: str
    redacted_text: str
    unsafe_spans: List[tuple[int, int]]

class ThresholdDecision(BaseModel):
    allow: bool
    reason: str
    scores: Dict[str, float]

class ModerationDecision(BaseModel):
    text: str
    decision: str
    categories: List[str]
    timestamp: str

class SummaryRequest(BaseModel):
    decisions: List[ModerationDecision]

class SummaryResponse(BaseModel):
    summary_text: str

class TranslationRequest(BaseModel):
    text: str
    target_language: str = "EN-US"

class TranslationResponse(BaseModel):
    original_text: str
    translated_text: str
    detected_source_lang: str

class EmbeddingRequest(BaseModel):
    text: str
    
class EmbeddingResponse(BaseModel):
    text: str
    embedding: List[float]

class AudioBriefRequest(BaseModel):
    text: str
    output_path: str
