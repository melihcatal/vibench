# Local request, response, and normalization helpers for Text Content Safety
from typing import List, Dict, Optional, TypedDict
from enum import Enum


class SafetyCategory(str, Enum):
    HATE = "hate"
    VIOLENCE = "violence"
    SEXUAL = "sexual"
    SELF_HARM = "self_harm"
    HARASSMENT = "harassment"
    DANGEROUS = "dangerous"


class SafetyDecision(TypedDict):
    allowed: bool
    categories: Dict[SafetyCategory, float]
    blocked_reason: Optional[str]


class RedactionSpan(TypedDict):
    start: int
    end: int
    category: SafetyCategory
    replacement: str


class ModerationResult(TypedDict):
    text: str
    decision: SafetyDecision
    redactions: List[RedactionSpan]
    provider: str


def normalize_scores(scores: Dict[str, float]) -> Dict[SafetyCategory, float]:
    """Normalize provider-specific category names to local enum."""
    category_mapping = {
        "hate": SafetyCategory.HATE,
        "hate/threatening": SafetyCategory.HATE,
        "violence": SafetyCategory.VIOLENCE,
        "violence/graphic": SafetyCategory.VIOLENCE,
        "sexual": SafetyCategory.SEXUAL,
        "sexual/minors": SafetyCategory.SEXUAL,
        "self-harm": SafetyCategory.SELF_HARM,
        "self-harm/intent": SafetyCategory.SELF_HARM,
        "self-harm/instructions": SafetyCategory.SELF_HARM,
        "harassment": SafetyCategory.HARASSMENT,
        "harassment/threatening": SafetyCategory.HARASSMENT,
        "dangerous": SafetyCategory.DANGEROUS,
    }
    normalized = {}
    for provider_key, score in scores.items():
        if provider_key in category_mapping:
            category = category_mapping[provider_key]
            if category not in normalized or score > normalized[category]:
                normalized[category] = score
    return normalized