from typing import Dict

from safety_client import build_perspective_payload, post_moderation
from safety_models import ModerationRequest, ThresholdDecision


def safety_threshold(
    request: ModerationRequest, thresholds: Dict[str, float]
) -> ThresholdDecision:
    raw = post_moderation(
        build_perspective_payload(
            request.text, [request.language] if request.language else None
        )
    )
    scores = {k: float(v) for k, v in raw.get("attributeScores", {}).items()}
    triggered = [k for k, v in scores.items() if v >= float(thresholds.get(k, 1.0))]
    return ThresholdDecision(
        allowed=not triggered, triggered_categories=triggered, scores=scores, raw=raw
    )
