from typing import Dict, List, Optional, Union, TypedDict
from enum import Enum


class TextCategory(str, Enum):
    HATE = "Hate"
    SELF_HARM = "SelfHarm"
    SEXUAL = "Sexual"
    VIOLENCE = "Violence"


class DetectedTextItem(TypedDict):
    text: str
    category: str
    severity: int
    start_index: int
    end_index: int
    blocklist_name: Optional[str]


class ModerationResult(TypedDict):
    decision: bool
    scores: Dict[str, int]
    category_decisions: Optional[Dict[str, bool]]


class RedactionResult(TypedDict):
    redacted_text: str
    detected_spans: List[DetectedTextItem]
    decision: bool


def normalize_scores(scores: Dict[str, int]) -> Dict[str, int]:
    """Normalize scores to a 0-6 scale if needed."""
    normalized = {}
    for category, score in scores.items():
        normalized[category] = min(max(score, 0), 6)
    return normalized


def normalize_categories(categories: Optional[List[str]]) -> List[str]:
    """Ensure categories are valid and normalized."""
    valid_categories = {"Hate", "SelfHarm", "Sexual", "Violence"}
    if not categories:
        return list(valid_categories)
    return [cat for cat in categories if cat in valid_categories]
