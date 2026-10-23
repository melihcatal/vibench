import os
from safety_client import SafetyClient


def moderate_batch(texts: list[str]) -> list[dict]:
    """Score a batch of user messages using Anthropic.
    Returns a list of dicts for each message containing decision/rationale.
    """
    client = SafetyClient()
    responses = client.moderate_batch(messages=texts)
    return [
        {
            "decision": resp["decision"],
            "rationale": resp.get("rationale", ""),
        }
        for resp in responses
    ]
