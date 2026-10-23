from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class ModerationRequest:
    text: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ModerationDecision:
    allow: bool
    category: str
    severity: float
    redacted_text: Optional[str] = None
    rationale: Optional[str] = None
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class BatchModerationResult:
    decisions: List[ModerationDecision]


@dataclass
class ThresholdConfig:
    thresholds: Dict[str, float]
    default_threshold: float = 0.5


def normalize_severity(value: Any) -> float:
    if value is None:
        return 0.0
    if isinstance(value, str):
        lookup = {"safe": 0.0, "low": 0.25, "medium": 0.5, "high": 0.9, "very_high": 1.0}
        if value.lower() in lookup:
            return lookup[value.lower()]
        try:
            return float(value)
        except ValueError:
            return 0.0
    if isinstance(value, bool):
        return 1.0 if value else 0.0
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def extract_category_scores(payload: Dict[str, Any]) -> Dict[str, float]:
    categories: Dict[str, float] = {}
    for key in ("categories", "categoryScores", "scores"):
        candidate = payload.get(key)
        if isinstance(candidate, dict):
            for name, score in candidate.items():
                categories[str(name)] = normalize_severity(score)
    return categories


def best_category(scores: Dict[str, float]) -> str:
    if not scores:
        return "unknown"
    return max(scores, key=scores.get)


def redact_spans(text: str, spans: Iterable[Dict[str, Any]]) -> str:
    ordered = sorted(spans, key=lambda s: int(s.get("offset", 0)))
    out = []
    last = 0
    for span in ordered:
        start = int(span.get("offset", 0))
        length = int(span.get("length", 0))
        out.append(text[last:start])
        out.append("[REDACTED]")
        last = start + length
    out.append(text[last:])
    return "".join(out)
