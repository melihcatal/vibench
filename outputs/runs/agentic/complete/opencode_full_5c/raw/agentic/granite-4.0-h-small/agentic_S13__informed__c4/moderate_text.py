import os
from safety_client import SafetyClient


def moderate_text(user_text: str) -> dict:
    """Score a single user text for unsafe or policy-violating content using Anthropic.
    Returns a dict with decision and rationale.
    """
    client = SafetyClient()  # uses environment variables for Anthropic
    response = client.moderate(text=user_text)
    return {
        "decision": response["decision"],
        "rationale": response.get("rationale", ""),
    }
