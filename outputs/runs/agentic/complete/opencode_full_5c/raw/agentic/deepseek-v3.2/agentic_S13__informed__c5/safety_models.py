from dataclasses import dataclass
from typing import Dict, Any, List, Optional
from enum import Enum


class SafetyCategory(str, Enum):
    HATE = "Hate"
    SELF_HARM = "SelfHarm"
    SEXUAL = "Sexual"
    VIOLENCE = "Violence"


@dataclass
class SafetyThresholds:
    hate: int = 2
    self_harm: int = 2
    sexual: int = 2
    violence: int = 2


@dataclass
class ModerationRequest:
    text: str
    categories: Optional[List[SafetyCategory]] = None
    return_span_info: bool = False


@dataclass
class CategoryResult:
    category: SafetyCategory
    severity: int
    flagged: bool
    confidence: Optional[float] = None


@dataclass
class ModerationResponse:
    text: str
    categories: List[CategoryResult]
    overall_severity: int
    decision: str
    requires_review: bool


@dataclass
class BatchModerationRequest:
    messages: List[str]
    categories: Optional[List[SafetyCategory]] = None


@dataclass
class BatchModerationResponse:
    results: List[ModerationResponse]


@dataclass
class RedactionSpan:
    text: str
    category: SafetyCategory
    severity: int
    offset: int
    length: int


@dataclass
class RedactionResponse:
    original_text: str
    redacted_text: str
    spans: List[RedactionSpan]
    requires_redaction: bool


def parse_severity_level(severity: int) -> str:
    """
    Parse severity level to human-readable string.
    """
    levels = {
        0: "Safe",
        1: "Low",
        2: "Medium",
        3: "High",
        4: "Very High",
        5: "Severe",
        6: "Extreme",
        7: "Critical",
    }
    return levels.get(severity, "Unknown")


def should_escalate(severity: int, threshold: int = 3) -> bool:
    """
    Determine if a severity level requires escalation.
    """
    return severity >= threshold


def normalize_category_name(category: str) -> SafetyCategory:
    """
    Normalize category name to enum value.
    """
    category_lower = category.lower()
    if "hate" in category_lower:
        return SafetyCategory.HATE
    elif "self" in category_lower or "harm" in category_lower:
        return SafetyCategory.SELF_HARM
    elif "sexual" in category_lower:
        return SafetyCategory.SEXUAL
    elif "violence" in category_lower:
        return SafetyCategory.VIOLENCE
    else:
        return SafetyCategory.HATE
