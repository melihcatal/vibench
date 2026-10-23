from __future__ import annotations

from typing import Dict

from safety_models import ModerationDecision, ThresholdConfig
from moderate_text import moderate_text


CATEGORY_ALIASES: Dict[str, str] = {
    "selfharm": "self_harm",
    "self_harm": "self_harm",
    "hate": "hate",
    "sexual": "sexual",
    "violence": "violence",
}


def apply_safety_threshold(text: str, thresholds: ThresholdConfig | None = None) -> ModerationDecision:
    thresholds = thresholds or ThresholdConfig()
    decision = moderate_text(text)
    threshold_map = thresholds.as_dict()
    allowed = True
    for category in decision.categories:
        key = CATEGORY_ALIASES.get(category.category.replace("-", "").replace(" ", "_"), category.category)
        limit = threshold_map.get(key, 4.0)
        if category.score >= limit or category.blocked:
            allowed = False
            break
    decision.allowed = allowed
    decision.reason = "azure_ai_content_safety_threshold_check"
    return decision
