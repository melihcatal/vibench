from __future__ import annotations

from safety_client import SafetyClient
from safety_models import ModerationRequest

PERSPECTIVE_MODEL = "Perspective API toxicity/comment analysis"


def safety_threshold(text: str, thresholds: dict[str, float] | None = None) -> dict:
    client = SafetyClient()
    thresholds = thresholds or {"TOXICITY": 0.35, "SEVERE_TOXICITY": 0.2, "INSULT": 0.4}
    decision = client.apply_thresholds(ModerationRequest(text=text), thresholds)
    return {
        "provider": "Perspective API",
        "model": PERSPECTIVE_MODEL,
        "allowed": decision.allowed,
        "categories": [c.__dict__ for c in decision.categories],
        "thresholds": thresholds,
    }
