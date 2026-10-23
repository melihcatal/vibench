from typing import Dict, Any, List, Optional
from pydantic import BaseModel


class ModerationResult(BaseModel):
    hate: int = 0
    self_harm: int = 0
    sexual: int = 0
    violence: int = 0
    redacted_text: Optional[str] = None


class SafetyDecision(BaseModel):
    allow: bool
    blocked_categories: List[str] = []
    scores: Dict[str, int] = {}


def normalize_moderation_result(raw_result: Dict[str, Any]) -> ModerationResult:
    """Normalize raw Azure AI Content Safety result into a structured model."""
    return ModerationResult(
        hate=raw_result.get("hate", 0),
        self_harm=raw_result.get("self_harm", 0),
        sexual=raw_result.get("sexual", 0),
        violence=raw_result.get("violence", 0),
        redacted_text=raw_result.get("redacted_text")
    )