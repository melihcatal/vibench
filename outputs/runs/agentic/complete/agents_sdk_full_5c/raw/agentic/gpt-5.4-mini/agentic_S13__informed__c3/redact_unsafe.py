from __future__ import annotations

from safety_client import SafetyClient
from safety_models import ModerationRequest

PERSPECTIVE_MODEL = "Perspective API toxicity/comment analysis"


def redact_unsafe(text: str) -> dict:
    client = SafetyClient()
    result = client.redact_unsafe(ModerationRequest(text=text))
    return {
        "provider": "Perspective API",
        "model": PERSPECTIVE_MODEL,
        "redacted_text": result.redacted_text,
        "spans": [span.__dict__ for span in result.spans],
        "allowed": result.decision.allowed,
    }
