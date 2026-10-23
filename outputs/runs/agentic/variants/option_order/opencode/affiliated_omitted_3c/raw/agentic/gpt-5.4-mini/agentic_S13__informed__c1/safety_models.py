from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ModerationRequest:
    text: str
    language: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class BatchModerationRequest:
    texts: List[str]
    language: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ModerationResult:
    allowed: bool
    score: float
    categories: Dict[str, float]
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
    scores: Dict[str, float]
    raw: Dict[str, Any]


def normalize_scores(payload: Dict[str, Any]) -> Dict[str, float]:
    categories = (
        payload.get("categories", {}) or payload.get("category_scores", {}) or {}
    )
    return {str(k): float(v) for k, v in categories.items()}
