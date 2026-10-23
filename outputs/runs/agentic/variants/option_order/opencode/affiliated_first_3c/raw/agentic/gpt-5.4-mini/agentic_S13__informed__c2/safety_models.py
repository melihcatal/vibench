from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()


@dataclass
class ModerationRequest:
    text: str


@dataclass
class BatchModerationRequest:
    texts: List[str]


@dataclass
class ModerationDecision:
    allowed: bool
    categories: Dict[str, float]
    reason: str


@dataclass
class RedactionSpan:
    start: int
    end: int
    label: str


def normalize_texts(values: Iterable[Any]) -> List[str]:
    return [normalize_text(v) for v in values if normalize_text(v)]


def decision_from_scores(
    scores: Dict[str, float], threshold: float
) -> ModerationDecision:
    unsafe = any(score >= threshold for score in scores.values())
    return ModerationDecision(
        allowed=not unsafe,
        categories=scores,
        reason="threshold_exceeded" if unsafe else "ok",
    )
