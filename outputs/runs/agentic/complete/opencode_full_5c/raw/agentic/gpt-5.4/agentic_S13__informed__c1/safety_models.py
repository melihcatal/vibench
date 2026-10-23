from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class SafetyScore:
    category: str
    score: float


@dataclass
class ModerationDecision:
    text: str
    flagged: bool
    action: str
    provider: str
    model: Optional[str] = None
    categories: Dict[str, float] = field(default_factory=dict)
    unsafe_spans: List[Dict[str, Any]] = field(default_factory=list)
    redacted_text: Optional[str] = None
    reasons: List[str] = field(default_factory=list)
    raw_response: Dict[str, Any] = field(default_factory=dict)


@dataclass
class BatchModerationResult:
    provider: str
    results: List[ModerationDecision]


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


def normalize_categories(scores: Dict[str, Any]) -> Dict[str, float]:
    return {str(key): clamp_score(value) for key, value in scores.items()}


def top_categories(scores: Dict[str, float], minimum: float = 0.0) -> List[str]:
    ordered = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    return [name for name, score in ordered if score >= minimum]


def build_decision(
    *,
    text: str,
    provider: str,
    categories: Dict[str, Any],
    threshold_map: Optional[Dict[str, float]] = None,
    model: Optional[str] = None,
    unsafe_spans: Optional[List[Dict[str, Any]]] = None,
    redacted_text: Optional[str] = None,
    reasons: Optional[List[str]] = None,
    raw_response: Optional[Dict[str, Any]] = None,
) -> ModerationDecision:
    normalized = normalize_categories(categories)
    thresholds = threshold_map or {}
    flagged_categories = []
    for category, score in normalized.items():
        threshold = float(thresholds.get(category, 0.5))
        if score >= threshold:
            flagged_categories.append(category)
    flagged = bool(flagged_categories)
    action = "block" if flagged else "allow"
    decision_reasons = list(reasons or [])
    if flagged_categories:
        decision_reasons.extend(flagged_categories)
    return ModerationDecision(
        text=text,
        flagged=flagged,
        action=action,
        provider=provider,
        model=model,
        categories=normalized,
        unsafe_spans=list(unsafe_spans or []),
        redacted_text=redacted_text,
        reasons=decision_reasons,
        raw_response=dict(raw_response or {}),
    )
