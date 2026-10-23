from typing import Dict

from safety_models import SafetyDecision


def safety_threshold(
    scores: Dict[str, float], thresholds: Dict[str, float]
) -> SafetyDecision:
    allow = True
    for category, score in scores.items():
        threshold = thresholds.get(category, 1.0)
        if score >= threshold:
            allow = False
    return SafetyDecision(
        allow=allow, scores=dict(scores), reason=None if allow else "threshold_exceeded"
    )
