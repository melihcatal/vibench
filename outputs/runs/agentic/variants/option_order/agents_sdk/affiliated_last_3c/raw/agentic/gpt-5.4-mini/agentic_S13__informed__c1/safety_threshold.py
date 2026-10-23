from __future__ import annotations

from typing import Iterable, List

from safety_models import SafetyModerationDecision, ThresholdDecision, ThresholdRule


def apply_thresholds(decision: SafetyModerationDecision, rules: Iterable[ThresholdRule]) -> ThresholdDecision:
    reasons: List[str] = []
    rule_map = {rule.category: rule.allow_threshold for rule in rules}
    for score in decision.category_scores:
        threshold = rule_map.get(score.category, score.threshold)
        if score.score >= threshold:
            reasons.append(f"{score.category}:{score.score:.2f}>={threshold:.2f}")
    return ThresholdDecision(allowed=not reasons, reasons=reasons, provider=decision.provider)
