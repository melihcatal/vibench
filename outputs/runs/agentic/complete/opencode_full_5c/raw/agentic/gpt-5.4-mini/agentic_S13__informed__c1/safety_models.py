from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


def normalize_text(text: Optional[str]) -> str:
    return (text or "").strip()


def normalize_category_scores(scores: Optional[Dict[str, Any]]) -> Dict[str, float]:
    result = {}
    for key, value in (scores or {}).items():
        try:
            result[str(key)] = float(value)
        except (TypeError, ValueError):
            continue
    return result


@dataclass
class ModerationRequest:
    text: str


@dataclass
class BatchModerationRequest:
    texts: List[str] = field(default_factory=list)


@dataclass
class ModerationDecision:
    allowed: bool
    score: float = 0.0
    categories: Dict[str, float] = field(default_factory=dict)
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RedactionSpan:
    start: int
    end: int
    category: str


@dataclass
class RedactionResult:
    text: str
    spans: List[RedactionSpan] = field(default_factory=list)
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ThresholdRule:
    category: str
    threshold: float


@dataclass
class ThresholdDecision:
    allowed: bool
    triggered: List[str] = field(default_factory=list)
    categories: Dict[str, float] = field(default_factory=dict)
    raw: Dict[str, Any] = field(default_factory=dict)
