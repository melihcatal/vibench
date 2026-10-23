from typing import List, Dict, Optional, TypedDict, Any


class SafetyCategory(TypedDict):
    category: str
    score: float


class ModerationDecision(TypedDict):
    input_text: str
    flagged: bool
    categories: List[SafetyCategory]
    details: Optional[Dict[str, Any]]


class BatchModerationDecision(TypedDict):
    decisions: List[ModerationDecision]


class UnsafeSpan(TypedDict):
    start: int
    end: int
    category: str
    score: float


class RedactionResult(TypedDict):
    original_text: str
    redacted_text: str
    spans: List[UnsafeSpan]
