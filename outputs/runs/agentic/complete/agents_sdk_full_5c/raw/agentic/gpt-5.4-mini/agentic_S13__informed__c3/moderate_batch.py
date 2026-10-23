from __future__ import annotations

from safety_client import SafetyClient
from safety_models import BatchModerationRequest, ModerationRequest

PERSPECTIVE_MODEL = "Perspective API toxicity/comment analysis"


def moderate_batch(messages: list[str]) -> list[dict]:
    client = SafetyClient()
    request = BatchModerationRequest(messages=[ModerationRequest(text=m) for m in messages])
    results = client.moderate_batch(request)
    return [
        {
            "provider": "Perspective API",
            "model": PERSPECTIVE_MODEL,
            "text": result.text,
            "allowed": result.decision.allowed,
            "categories": [c.__dict__ for c in result.decision.categories],
        }
        for result in results
    ]
