from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class SafetyCategoryScore:
    name: str
    score: float
    blocked: bool = False


@dataclass
class SafetyDecision:
    provider: str
    allowed: bool
    action: str
    categories: List[SafetyCategoryScore] = field(default_factory=list)
    redacted_text: Optional[str] = None
    flagged_spans: List[Dict[str, Any]] = field(default_factory=list)
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ModerationItem:
    text: str
    user_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ModerationBatchResult:
    provider: str
    results: List[SafetyDecision]


def clamp_score(value: Any) -> float:
    try:
        score = float(value)
    except (TypeError, ValueError):
        return 0.0
    if score < 0.0:
        return 0.0
    if score > 1.0:
        return 1.0
    return score


def normalize_hive_class(class_name: str) -> str:
    return class_name.strip().lower().replace(" ", "_")


def ensure_text(text: str) -> str:
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    return text


def serialize_decision(decision: SafetyDecision) -> Dict[str, Any]:
    return {
        "provider": decision.provider,
        "allowed": decision.allowed,
        "action": decision.action,
        "categories": [
            {"name": item.name, "score": item.score, "blocked": item.blocked}
            for item in decision.categories
        ],
        "redacted_text": decision.redacted_text,
        "flagged_spans": decision.flagged_spans,
        "raw": decision.raw,
    }


def summarize_actions(decisions: List[SafetyDecision]) -> Dict[str, int]:
    counts: Dict[str, int] = {"allow": 0, "review": 0, "block": 0, "redact": 0}
    for item in decisions:
        counts[item.action] = counts.get(item.action, 0) + 1
    return counts
