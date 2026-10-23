from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class SafetySpan:
    start: int
    end: int
    label: str
    text: str = ""
    score: float = 0.0


@dataclass
class SafetyDecision:
    allowed: bool
    action: str
    flagged_categories: List[str] = field(default_factory=list)
    scores: Dict[str, float] = field(default_factory=dict)
    spans: List[SafetySpan] = field(default_factory=list)
    provider: str = ""
    raw: Optional[Dict[str, Any]] = None


@dataclass
class SafetyRequest:
    text: str
    language: str = "en"
    user_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


def clamp_score(value: Any) -> float:
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return 0.0
    if numeric < 0.0:
        return 0.0
    if numeric > 1.0:
        return 1.0
    return numeric


def normalize_category_scores(categories: Dict[str, Any]) -> Dict[str, float]:
    return {str(name): clamp_score(score) for name, score in categories.items()}


def normalize_spans(items: List[Dict[str, Any]]) -> List[SafetySpan]:
    spans: List[SafetySpan] = []
    for item in items:
        spans.append(
            SafetySpan(
                start=int(item.get("start", 0)),
                end=int(item.get("end", 0)),
                label=str(item.get("label", "unsafe")),
                text=str(item.get("text", "")),
                score=clamp_score(item.get("score", 0.0)),
            )
        )
    return spans


def decision_dict(decision: SafetyDecision) -> Dict[str, Any]:
    return {
        "allowed": decision.allowed,
        "action": decision.action,
        "flagged_categories": list(decision.flagged_categories),
        "scores": dict(decision.scores),
        "spans": [span.__dict__ for span in decision.spans],
        "provider": decision.provider,
        "raw": decision.raw,
    }
