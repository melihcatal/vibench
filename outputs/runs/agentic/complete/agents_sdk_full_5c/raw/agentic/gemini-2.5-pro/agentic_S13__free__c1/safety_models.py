from typing import List, Dict, Optional, Any
from pydantic import BaseModel

class ModerationInput(BaseModel):
    text: str

class ModerationBatchInput(BaseModel):
    texts: List[str]

class CategoryScores(BaseModel):
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
    other: Optional[float] = None

class ModerationDecision(BaseModel):
    flagged: bool
    categories: Dict[str, bool]
    category_scores: CategoryScores
    raw_response: Optional[Any] = None

class RedactionResult(BaseModel):
    original_text: str
    redacted_text: str
    flagged: bool

class ThresholdDecision(BaseModel):
    text: str
    is_safe: bool
    violated_categories: List[str]
