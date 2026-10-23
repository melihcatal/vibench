from __future__ import annotations

from safety_client import SafetyClient
from safety_models import ModerationRequest

PERSPECTIVE_MODEL = "Perspective API toxicity/comment analysis"


def moderate_text(text: str) -> dict:
    client = SafetyClient()
    result = client.moderate(ModerationRequest(text=text))
    return {
        "provider": "Perspective API",
        "model": PERSPECTIVE_MODEL,
        "allowed": result.decision.allowed,
        "categories": [c.__dict__ for c in result.decision.categories],
    }
