from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class SafetyRequest:
    text: str
    language: str = "en"
    user_id: Optional[str] = None


@dataclass
class CategoryScore:
    name: str
    score: float


@dataclass
class SafetyResult:
    text: str
    allow: bool
    flagged: bool
    categories: List[CategoryScore] = field(default_factory=list)
    provider: str = ""
    model: str = ""
    redacted_text: Optional[str] = None
    unsafe_spans: List[Dict[str, Any]] = field(default_factory=list)
    raw: Dict[str, Any] = field(default_factory=dict)


def normalize_perspective_scores(response: Dict[str, Any]) -> List[CategoryScore]:
    attribute_scores = response.get("attributeScores", {})
    normalized: List[CategoryScore] = []
    for name, payload in attribute_scores.items():
        summary = payload.get("summaryScore", {})
        value = float(summary.get("value", 0.0))
        normalized.append(CategoryScore(name=name.lower(), score=value))
    return normalized


def scores_to_dict(scores: List[CategoryScore]) -> Dict[str, float]:
    return {item.name: item.score for item in scores}


def to_serializable_result(result: SafetyResult) -> Dict[str, Any]:
    return {
        "text": result.text,
        "allow": result.allow,
        "flagged": result.flagged,
        "categories": [{"name": c.name, "score": c.score} for c in result.categories],
        "provider": result.provider,
        "model": result.model,
        "redacted_text": result.redacted_text,
        "unsafe_spans": result.unsafe_spans,
        "raw": result.raw,
    }
