# Local request, response, and normalization helpers for Text Content Safety

from typing import List, Dict, Optional, TypedDict
from enum import Enum


class SafetyCategory(str, Enum):
    HATE = "hate"
    SEXUAL = "sexual"
    VIOLENCE = "violence"
    SELF_HARM = "self_harm"
    HARASSMENT = "harassment"
    DANGEROUS = "dangerous"


class SafetyDecision(TypedDict):
    category: SafetyCategory
    score: float
    flagged: bool
    threshold: Optional[float]


class TextModerationRequest(TypedDict):
    text: str
    categories: Optional[List[SafetyCategory]]
    threshold_overrides: Optional[Dict[SafetyCategory, float]]


class TextModerationResponse(TypedDict):
    decisions: List[SafetyDecision]
    raw_response: Dict


class RedactionSpan(TypedDict):
    start: int
    end: int
    category: SafetyCategory
    replacement: Optional[str]


class RedactionResponse(TypedDict):
    redacted_text: str
    spans: List[RedactionSpan]
    raw_response: Dict


def normalize_safety_decision(raw_decision: Dict, threshold_overrides: Optional[Dict[SafetyCategory, float]] = None) -> SafetyDecision:
    """Normalize raw provider response into a standardized SafetyDecision."""
    category = SafetyCategory(raw_decision["category"])
    score = raw_decision["score"]
    threshold = threshold_overrides.get(category) if threshold_overrides else raw_decision.get("threshold", 0.5)
    flagged = score >= threshold
    return {
        "category": category,
        "score": score,
        "flagged": flagged,
        "threshold": threshold,
    }