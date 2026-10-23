from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()


def normalize_language(value: Any) -> Optional[str]:
    text = normalize_text(value)
    return text or None


@dataclass
class SafetyRequest:
    text: str
    language: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SafetyBatchRequest:
    messages: List[str]
    language: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SafetyDecision:
    allowed: bool
    categories: Dict[str, float]
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RedactionResult:
    text: str
    redactions: List[Dict[str, Any]]
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ThresholdRule:
    category: str
    threshold: float


def coerce_thresholds(values: Optional[Dict[str, Any]]) -> Dict[str, float]:
    if not values:
        return {}
    return {str(k): float(v) for k, v in values.items()}
