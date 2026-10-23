from __future__ import annotations

from typing import Dict

from safety_models import SafetyDecision


DEFAULT_THRESHOLDS: Dict[str, float] = {
    "hate_speech": 0.6,
    "violence": 0.75,
    "sexual": 0.8,
    "harassment": 0.65,
}


def apply_safety_threshold(
    decision: SafetyDecision, thresholds: Dict[str, float] | None = None
) -> SafetyDecision:
    merged = dict(DEFAULT_THRESHOLDS)
    if thresholds:
        merged.update(thresholds)
    blocked = False
    updated = []
    for item in decision.categories:
        limit = merged.get(item.name, 0.7)
        item.blocked = item.score >= limit
        blocked = blocked or item.blocked
        updated.append(item)
    decision.categories = updated
    decision.allowed = not blocked
    decision.action = "block" if blocked else "allow"
    return decision
