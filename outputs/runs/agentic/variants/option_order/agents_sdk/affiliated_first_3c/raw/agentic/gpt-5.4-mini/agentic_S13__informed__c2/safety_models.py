from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Sequence


@dataclass(frozen=True)
class ModerationDecision:
    allowed: bool
    category: str
    severity: float
    reason: str


@dataclass(frozen=True)
class RedactionSpan:
    start: int
    end: int
    label: str


@dataclass(frozen=True)
class ThresholdRule:
    category: str
    max_severity: float


def normalize_score(value: Any) -> float:
    try:
        return max(0.0, min(1.0, float(value)))
    except (TypeError, ValueError):
        return 0.0


def parse_thresholds(items: Sequence[Dict[str, Any]]) -> List[ThresholdRule]:
    return [ThresholdRule(category=str(i.get("category", "")), max_severity=normalize_score(i.get("max_severity", 0.5))) for i in items]


def decision_from_result(category: str, severity: Any, reason: str = "") -> ModerationDecision:
    sev = normalize_score(severity)
    return ModerationDecision(allowed=sev < 0.5, category=category, severity=sev, reason=reason or category)
