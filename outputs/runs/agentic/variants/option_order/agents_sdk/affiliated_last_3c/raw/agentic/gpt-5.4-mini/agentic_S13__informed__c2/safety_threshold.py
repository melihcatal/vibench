from __future__ import annotations

from typing import Mapping

from safety_models import ThresholdRule, is_unsafe


def apply_thresholds(scores: Mapping[str, float], rules: list[ThresholdRule] | None = None) -> bool:
    if rules is None:
        return not is_unsafe(scores, threshold=0.5)
    for rule in rules:
        if scores.get(rule.category, 0.0) >= rule.allow_below:
            return False
    return True
