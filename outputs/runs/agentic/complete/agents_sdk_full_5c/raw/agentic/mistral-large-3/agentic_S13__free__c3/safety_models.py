from typing import List, Dict, Optional, TypedDict
from enum import Enum


class SafetyCategory(str, Enum):
    HATE = "hate"
    VIOLENCE = "violence"
    SEXUAL = "sexual"
    SELF_HARM = "self_harm"
    HARASSMENT = "harassment"
    DANGEROUS = "dangerous"


class SafetySeverity(str, Enum):
    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class SafetySpan(TypedDict):
    start: int
    end: int
    category: SafetyCategory
    severity: SafetySeverity
    confidence: float


class ModerationDecision(TypedDict):
    allowed: bool
    categories: Dict[SafetyCategory, bool]
    scores: Dict[SafetyCategory, float]
    spans: List[SafetySpan]


class TextModerationRequest(TypedDict):
    text: str
    categories: Optional[List[SafetyCategory]]
    threshold: Optional[Dict[SafetyCategory, float]]


class BatchModerationRequest(TypedDict):
    texts: List[str]
    categories: Optional[List[SafetyCategory]]
    threshold: Optional[Dict[SafetyCategory, float]]


def normalize_category(category: str) -> SafetyCategory:
    category_map = {
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
    return category_map.get(category.lower(), SafetyCategory.HATE)


def normalize_severity(severity: str) -> SafetySeverity:
    severity_map = {
        "none": SafetySeverity.NONE,
        "low": SafetySeverity.LOW,
        "medium": SafetySeverity.MEDIUM,
        "high": SafetySeverity.HIGH,
    }
    return severity_map.get(severity.lower(), SafetySeverity.NONE)