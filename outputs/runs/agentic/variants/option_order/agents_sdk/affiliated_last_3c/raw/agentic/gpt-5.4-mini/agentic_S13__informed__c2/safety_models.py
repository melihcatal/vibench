from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple


CATEGORY_NAMES = (
    "hate",
    "harassment",
    "self_harm",
    "sexual",
    "violence",
)


@dataclass
class CategoryScore:
    name: str
    score: float


@dataclass
class ModerationRequest:
    text: str
    language: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ModerationDecision:
    flagged: bool
    scores: Dict[str, float]
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class BatchModerationResult:
    decisions: List[ModerationDecision]


@dataclass
class RedactionSpan:
    start: int
    end: int
    label: str


@dataclass
class ThresholdRule:
    category: str
    allow_below: float


@dataclass
class TextSafetyConfig:
    api_key: str
    endpoint: str = "https://api.perspectiveapi.com/v1alpha1/comments:analyze"
    timeout_seconds: int = 30


def normalize_text(text: str) -> str:
    return " ".join((text or "").split())


def clamp_score(value: Any) -> float:
    try:
        score = float(value)
    except (TypeError, ValueError):
        score = 0.0
    return max(0.0, min(1.0, score))


def scores_from_mapping(mapping: Mapping[str, Any]) -> Dict[str, float]:
    return {k: clamp_score(v) for k, v in mapping.items() if k}


def is_unsafe(scores: Mapping[str, float], threshold: float = 0.5) -> bool:
    return any(v >= threshold for v in scores.values())
