from __future__ import annotations

from typing import Dict, Mapping

from safety_models import ThresholdDecision, ThresholdRule, normalize_scores


DEFAULT_RULES = (
    ThresholdRule(category="toxicity", threshold=0.5),
    ThresholdRule(category="severe_toxicity", threshold=0.4),
    ThresholdRule(category="insult", threshold=0.6),
    ThresholdRule(category="threat", threshold=0.35),
    ThresholdRule(category="profanity", threshold=0.7),
)


def apply_thresholds(category_scores: Mapping[str, float]) -> ThresholdDecision:
    scores = normalize_scores(category_scores)
    triggered: Dict[str, float] = {}
    allowed = True
    for rule in DEFAULT_RULES:
        score = scores.get(rule.category, 0.0)
        if score >= rule.threshold:
            triggered[rule.category] = score
            allowed = False
    return ThresholdDecision(allowed=allowed, triggered=triggered, raw=scores)
