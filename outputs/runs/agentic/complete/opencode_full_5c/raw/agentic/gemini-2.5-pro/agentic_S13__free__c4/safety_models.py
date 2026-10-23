from typing import List, Dict, Optional
from pydantic import BaseModel, Field


class ModerationAttributes(BaseModel):
    toxicity: Optional[float] = None
    severe_toxicity: Optional[float] = Field(default=None, alias="SEVERE_TOXICITY")
    identity_attack: Optional[float] = Field(default=None, alias="IDENTITY_ATTACK")
    insult: Optional[float] = Field(default=None, alias="INSULT")
    profanity: Optional[float] = Field(default=None, alias="PROFANITY")
    threat: Optional[float] = Field(default=None, alias="THREAT")


class ModerationDecision(BaseModel):
    flagged: bool
    scores: ModerationAttributes
    text: str


class BatchModerationDecision(BaseModel):
    decisions: List[ModerationDecision]


class RedactionResult(BaseModel):
    original_text: str
    redacted_text: str
    redactions_found: int


class SafetyThresholdDecision(BaseModel):
    text: str
    is_allowed: bool
    flagged_categories: Dict[str, float]


class ModerationSummary(BaseModel):
    summary_text: str


class TranslationResult(BaseModel):
    original_text: str
    translated_text: str
    target_language: str


class EmbeddingResult(BaseModel):
    text: str
    embedding: List[float]


class AudioBriefResult(BaseModel):
    text: str
    audio_file_path: str
