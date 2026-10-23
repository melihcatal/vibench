from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class SafetyRequest:
    text: str
    user_id: Optional[str] = None
    language: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SafetyDecision:
    allowed: bool
    categories: Dict[str, float] = field(default_factory=dict)
    rationale: Optional[str] = None
    provider_response: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SafetyBatchItem:
    index: int
    text: str
    decision: SafetyDecision


def normalize_text(text: str) -> str:
    return " ".join((text or "").split())


def normalize_thresholds(thresholds: Optional[Dict[str, float]]) -> Dict[str, float]:
    if not thresholds:
        return {}
    return {str(k): float(v) for k, v in thresholds.items()}


def decision_from_scores(
    scores: Dict[str, float], threshold: float = 0.5
) -> SafetyDecision:
    allowed = all(v < threshold for v in scores.values())
    return SafetyDecision(
        allowed=allowed, categories=dict(scores), rationale=None, provider_response={}
    )
