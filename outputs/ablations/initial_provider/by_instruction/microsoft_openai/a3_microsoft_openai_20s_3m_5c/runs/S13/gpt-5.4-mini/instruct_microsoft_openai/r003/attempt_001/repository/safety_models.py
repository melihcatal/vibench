from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


def normalize_text(text: Optional[str]) -> str:
    return (text or "").strip()


def normalize_texts(texts: Optional[List[str]]) -> List[str]:
    return [normalize_text(t) for t in (texts or [])]


@dataclass
class ModerationRequest:
    text: str


@dataclass
class BatchModerationRequest:
    texts: List[str] = field(default_factory=list)


@dataclass
class ModerationDecision:
    flagged: bool
    categories: Dict[str, bool] = field(default_factory=dict)
    category_scores: Dict[str, float] = field(default_factory=dict)
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RedactionSpan:
    start: int
    end: int
    label: str = "unsafe"


@dataclass
class RedactionResult:
    redacted_text: str
    spans: List[RedactionSpan] = field(default_factory=list)
    decision: Optional[ModerationDecision] = None


@dataclass
class ThresholdResult:
    allowed: bool
    triggered: Dict[str, float] = field(default_factory=dict)
    decision: Optional[ModerationDecision] = None
