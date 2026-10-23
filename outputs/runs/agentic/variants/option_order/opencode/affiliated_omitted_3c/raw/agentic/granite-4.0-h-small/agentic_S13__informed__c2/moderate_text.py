import json
from safety_client import SafetyClient


def moderate_text(user_text: str) -> dict:
    """Score a single user message for unsafe or policy‑violating content using Alibaba Content Moderation.

    Returns a dictionary with the moderation decision and any flagged categories.
    """
    client = SafetyClient()
    response = client.moderate(user_text)
    result = response.get("result", {})
    return {
        "text": user_text,
        "decision": result.get("decision", "UNKNOWN"),
        "flags": result.get("flags", []),
        "scores": result.get("scores", {}),
    }
