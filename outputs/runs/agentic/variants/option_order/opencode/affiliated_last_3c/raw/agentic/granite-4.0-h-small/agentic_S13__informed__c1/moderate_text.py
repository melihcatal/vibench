import json
import os
from safety_client import SafetyClient

# Example: using Amazon Comprehend (or Bedrock Guardrails) – provider flagged in client
CLIENT = SafetyClient()


def moderate_text(user_text: str) -> dict:
    """Score a single user text for unsafe or policy‑violating content.

    Returns a dict with the provider‑specific response.
    """
    response = CLIENT.analyze_sentiment(text=user_text)
    return response
