from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class SafetyCategoryDecision:
    category: str
    score: float
    threshold: float
    flagged: bool


@dataclass
class SafetyResult:
    flagged: bool
    categories: List[SafetyCategoryDecision] = field(default_factory=list)
    raw: Optional[Dict[str, Any]] = None


@dataclass
class BatchModerationResult:
    results: List[SafetyResult]


@dataclass
class RedactionSpan:
    start: int
    end: int
    label: str


@dataclass
class RedactionResult:
    redacted_text: str
    spans: List[RedactionSpan] = field(default_factory=list)
    raw: Optional[Dict[str, Any]] = None


@dataclass
class ThresholdRule:
    category: str
    threshold: float


def normalize_text(value: Any) -> str:
    return '' if value is None else str(value).strip()


def normalize_thresholds(values: Optional[Dict[str, Any]]) -> Dict[str, float]:
    if not values:
        return {}
    return {str(k): float(v) for k, v in values.items()}
