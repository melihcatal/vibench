from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Sequence


@dataclass(frozen=True)
class ModerationRequest:
    text: str


@dataclass(frozen=True)
class ModerationDecision:
    allowed: bool
    categories: Dict[str, float]
    raw: Dict[str, Any]


@dataclass(frozen=True)
class BatchModerationItem:
    index: int
    allowed: bool
    categories: Dict[str, float]
    raw: Dict[str, Any]


@dataclass(frozen=True)
class RedactionSpan:
    start: int
    end: int
    label: str


@dataclass(frozen=True)
class ThresholdRule:
    category: str
    threshold: float


def normalize_category_scores(raw: Dict[str, Any]) -> Dict[str, float]:
    scores: Dict[str, float] = {}
    for key, value in raw.items():
        try:
            scores[str(key)] = float(value)
        except (TypeError, ValueError):
            continue
    return scores


def threshold_allows(scores: Dict[str, float], rules: Sequence[ThresholdRule]) -> bool:
    for rule in rules:
        if scores.get(rule.category, 0.0) >= rule.threshold:
            return False
    return True


def redaction_markers(scores: Dict[str, float], cutoff: float = 0.5) -> List[str]:
    return [category for category, score in scores.items() if score >= cutoff]
