from __future__ import annotations

from typing import Dict

from safety_models import SafetyDecision


DEFAULT_THRESHOLDS: Dict[str, float] = {
    "toxicity": 0.75,
    "severe_toxicity": 0.6,
    "insult": 0.8,
    "profanity": 0.85,
    "threat": 0.45,
    "identity_attack": 0.55,
}


def apply_safety_threshold(
    decision: SafetyDecision, thresholds: Dict[str, float] | None = None
) -> SafetyDecision:
    active_thresholds = thresholds or DEFAULT_THRESHOLDS
    flagged = [
        category
        for category, score in decision.scores.items()
        if score >= active_thresholds.get(category, 1.0)
    ]
    decision.flagged_categories = flagged
    decision.allowed = not flagged
    decision.action = "allow" if decision.allowed else "block"
    return decision
