from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()


def normalize_thresholds(value: Optional[Dict[str, Any]]) -> Dict[str, float]:
    if not value:
        return {}
    return {str(k): float(v) for k, v in value.items()}


@dataclass
class SafetyRequest:
    text: str
    thresholds: Dict[str, float] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SafetyDecision:
    allowed: bool
    category: str
    score: float
    provider: str
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class BatchSafetyResult:
    decisions: List[SafetyDecision]


@dataclass
class RedactionResult:
    text: str
    spans: List[Dict[str, Any]] = field(default_factory=list)
    allowed: bool = True
