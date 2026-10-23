from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class TextModerationRequest:
    text: str
    language: Optional[str] = None


@dataclass
class BatchModerationRequest:
    messages: List[str]
    language: Optional[str] = None


@dataclass
class ThresholdRule:
    category: str
    threshold: float


@dataclass
class ModerationResult:
    flagged: bool
    category_scores: Dict[str, float]
    categories: Dict[str, bool]
    raw: Dict[str, Any]


@dataclass
class BatchModerationResult:
    results: List[ModerationResult]
    raw: Dict[str, Any]


@dataclass
class RedactionResult:
    redacted_text: str
    spans: List[Dict[str, Any]]
    raw: Dict[str, Any]


@dataclass
class ThresholdDecision:
    allowed: bool
    triggered_categories: List[str]
    raw: Dict[str, Any]


def normalize_category_scores(data: Dict[str, Any]) -> Dict[str, float]:
    return {str(k): float(v) for k, v in data.items() if v is not None}


def normalize_categories(data: Dict[str, Any]) -> Dict[str, bool]:
    return {str(k): bool(v) for k, v in data.items()}
