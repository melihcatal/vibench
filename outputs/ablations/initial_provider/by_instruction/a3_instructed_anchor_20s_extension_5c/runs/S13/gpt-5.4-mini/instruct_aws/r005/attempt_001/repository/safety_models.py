from dataclasses import dataclass
from typing import Any, Dict, List, Optional


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()


def normalize_categories(value: Any) -> Dict[str, float]:
    if not isinstance(value, dict):
        return {}
    out: Dict[str, float] = {}
    for key, score in value.items():
        try:
            out[str(key)] = float(score)
        except (TypeError, ValueError):
            continue
    return out


@dataclass
class SafetyDecision:
    allowed: bool
    category_scores: Dict[str, float]
    labels: List[str]
    provider: str
    raw: Optional[Dict[str, Any]] = None


@dataclass
class BatchSafetyDecision:
    decisions: List[SafetyDecision]
    provider: str


@dataclass
class RedactionResult:
    text: str
    spans: List[Dict[str, Any]]
    provider: str


@dataclass
class ThresholdDecision:
    allowed: bool
    triggered_categories: List[str]
    thresholds: Dict[str, float]
    provider: str
