from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()


def normalize_score(value: Any) -> float:
    try:
        score = float(value)
    except (TypeError, ValueError):
        score = 0.0
    if score < 0:
        return 0.0
    if score > 1:
        return 1.0
    return score


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
class ModerationDecision:
    allow: bool
    score: float
    categories: Dict[str, float] = field(default_factory=dict)
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RedactionSpan:
    start: int
    end: int
    label: str


@dataclass
class RedactionResult:
    text: str
    spans: List[RedactionSpan] = field(default_factory=list)
    raw: Dict[str, Any] = field(default_factory=dict)
