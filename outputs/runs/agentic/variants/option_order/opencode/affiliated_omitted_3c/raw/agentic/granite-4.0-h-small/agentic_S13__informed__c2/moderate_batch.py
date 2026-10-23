import json
from safety_client import SafetyClient


def moderate_batch(messages: list[str]) -> list[dict]:
    """Moderate a batch of user messages using Alibaba Content Moderation.

    Returns a list with one moderation result per message.
    """
    client = SafetyClient()
    responses = client.moderate_batch(messages)
    # Normalize each response to our internal schema (see safety_models.py)
    return [
        {
            "text": msg,
            "decision": resp.get("decision", "UNKNOWN"),
            "flags": resp.get("flags", []),
            "scores": resp.get("scores", {}),
        }
        for msg, resp in zip(messages, responses)
    ]
