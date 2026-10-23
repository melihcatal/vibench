from typing import Dict, Any, List
from pydantic import BaseModel, Field

class CategoryScore(BaseModel):
    """Represents the severity score for a single moderation category."""
    severity: int

class ModerationResult(BaseModel):
    """Represents the overall moderation result for a single piece of text."""
    is_safe: bool
    scores: Dict[str, CategoryScore]
    raw_response: Dict[str, Any] = Field(default_factory=dict)

class BatchModerationResult(BaseModel):
    """Represents the results for a batch moderation request."""
    results: Dict[str, ModerationResult]

class TranslationRequest(BaseModel):
    """Represents a request to translate text."""
    text: str
    target_language: str
    source_language: str | None = None

class EmbeddingRequest(BaseModel):
    """Represents a request to embed a list of texts."""
    texts: List[str]
