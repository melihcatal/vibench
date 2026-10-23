from __future__ import annotations

from typing import Dict

from safety_client import moderate_text_with_openai
from safety_models import SafetyDecision, category_score_map


def apply_safety_thresholds(text: str, thresholds: Dict[str, float]) -> SafetyDecision:
    decision = moderate_text_with_openai(text)
    scores = category_score_map(decision)
    threshold_hit = any(
        scores.get(name, 0.0) >= value for name, value in thresholds.items()
    )
    decision.flagged = decision.flagged or threshold_hit
    decision.action = "block" if decision.flagged else "allow"
    decision.raw["thresholds"] = thresholds
    decision.raw["threshold_hit"] = threshold_hit
    return decision
