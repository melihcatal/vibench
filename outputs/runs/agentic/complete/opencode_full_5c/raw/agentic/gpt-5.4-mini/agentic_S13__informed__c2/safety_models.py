from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class SafetyTextRequest:
    text: str
    categories: Optional[List[str]] = None
    language: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SafetyBatchRequest:
    messages: List[str]
    categories: Optional[List[str]] = None
    language: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SafetyDecision:
    allowed: bool
    score: float
    categories: Dict[str, float] = field(default_factory=dict)
    reasons: List[str] = field(default_factory=list)
    redacted_text: Optional[str] = None


def normalize_text(text: str) -> str:
    return " ".join((text or "").split())


def normalize_thresholds(thresholds: Optional[Dict[str, float]]) -> Dict[str, float]:
    return dict(thresholds or {})
