from __future__ import annotations

from safety_client import moderate_text_request
from safety_models import ModerationRequest, moderation_result_to_dict


def apply_safety_thresholds(
    text: str,
    category_thresholds: dict[str, float] | None = None,
    default_threshold: float = 0.7,
) -> dict:
    result = moderate_text_request(ModerationRequest(text=text), threshold=0.0)
    thresholds = {k.lower(): v for k, v in (category_thresholds or {}).items()}
    blocked = False
    triggered: dict[str, float] = {}
    for name, category in result.categories.items():
        limit = thresholds.get(name, default_threshold)
        if category.score >= limit:
            blocked = True
            triggered[name] = limit
            category.flagged = True
        else:
            category.flagged = False
    result.blocked = blocked
    result.action = "block" if blocked else "allow"
    payload = moderation_result_to_dict(result)
    payload["applied_thresholds"] = {
        **{k: default_threshold for k in result.categories},
        **thresholds,
    }
    payload["triggered_thresholds"] = triggered
    return payload
