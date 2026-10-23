import os
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class SafetyCategory(str, Enum):
    HATE = "Hate"
    SELF_HARM = "SelfHarm"
    SEXUAL = "Sexual"
    VIOLENCE = "Violence"


class SeverityLevel(int, Enum):
    SAFE = 0
    LOW = 2
    MEDIUM = 4
    HIGH = 6


@dataclass
class SafetyRequest:
    text: str
    categories: list[SafetyCategory] = field(
        default_factory=lambda: list(SafetyCategory)
    )
    output_type: str = "FourSeverityLevels"


@dataclass
class CategoryScore:
    category: SafetyCategory
    severity: SeverityLevel
    raw_score: float = 0.0


@dataclass
class SafetyResponse:
    text: str
    category_scores: list[CategoryScore]
    block_action: bool = False
    raw_response: Optional[dict] = None


@dataclass
class BatchSafetyRequest:
    texts: list[str]
    categories: list[SafetyCategory] = field(
        default_factory=lambda: list(SafetyCategory)
    )


@dataclass
class BatchSafetyResult:
    index: int
    text: str
    response: SafetyResponse


@dataclass
class BatchSafetyResponse:
    results: list[BatchSafetyResult]
    total_processed: int


@dataclass
class FlaggedSpan:
    start: int
    end: int
    category: SafetyCategory
    severity: SeverityLevel
    matched_text: str


@dataclass
class RedactionResult:
    original_text: str
    redacted_text: str
    flagged_spans: list[FlaggedSpan]
    category_scores: list[CategoryScore]


@dataclass
class ThresholdConfig:
    thresholds: dict[SafetyCategory, SeverityLevel] = field(
        default_factory=lambda: {
            SafetyCategory.HATE: SeverityLevel.LOW,
            SafetyCategory.SELF_HARM: SeverityLevel.LOW,
            SafetyCategory.SEXUAL: SeverityLevel.LOW,
            SafetyCategory.VIOLENCE: SeverityLevel.LOW,
        }
    )
    action: str = "block"


@dataclass
class ThresholdDecision:
    allowed: bool
    text: str
    violated_categories: list[SafetyCategory]
    exceeded_thresholds: dict[SafetyCategory, SeverityLevel]
    raw_scores: list[CategoryScore]
