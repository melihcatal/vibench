# Text Content Safety Models and Normalization Helpers
from typing import List, Dict, Optional, TypedDict
from dataclasses import dataclass
from enum import Enum


class SafetyCategory(str, Enum):
    HATE = "hate"
    VIOLENCE = "violence"
    SEXUAL = "sexual"
    SELF_HARM = "self_harm"
    HARASSMENT = "harassment"
    DANGEROUS = "dangerous"


@dataclass
class SafetyScore:
    category: SafetyCategory
    score: float
    

@dataclass
class TextModerationResult:
    blocked: bool
    scores: List[SafetyScore]
    flagged_categories: List[SafetyCategory]
    

@dataclass
class RedactionSpan:
    start: int
    end: int
    category: SafetyCategory
    replacement: Optional[str] = None


class ModerationRequest(TypedDict):
    text: str
    categories: Optional[List[SafetyCategory]]


class BatchModerationRequest(TypedDict):
    texts: List[str]
    categories: Optional[List[SafetyCategory]]


def normalize_category(category: str) -> SafetyCategory:
    """Normalize provider-specific category names to internal enum."""
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
    return category_map.get(category.lower(), SafetyCategory.DANGEROUS)


def normalize_scores(provider_scores: Dict[str, float]) -> List[SafetyScore]:
    """Normalize provider-specific scores to internal model."""
    return [
        SafetyScore(category=normalize_category(category), score=score)
        for category, score in provider_scores.items()
    ]