from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class ModerationRequest:
    text: str
    user_id: Optional[str] = None


@dataclass
class ModerationDecision:
    allowed: bool
    categories: Dict[str, bool] = field(default_factory=dict)
    scores: Dict[str, float] = field(default_factory=dict)
    model: Optional[str] = None
    raw: Optional[Dict[str, Any]] = None


@dataclass
class BatchModerationResult:
    decisions: List[ModerationDecision]


@dataclass
class RedactionResult:
    text: str
    redacted_spans: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class ThresholdPolicy:
    thresholds: Dict[str, float]


def normalize_text(text: Any) -> str:
    if text is None:
        return ""
    return " ".join(str(text).split())


def normalize_messages(messages: Iterable[Any]) -> List[str]:
    return [normalize_text(m) for m in messages]
