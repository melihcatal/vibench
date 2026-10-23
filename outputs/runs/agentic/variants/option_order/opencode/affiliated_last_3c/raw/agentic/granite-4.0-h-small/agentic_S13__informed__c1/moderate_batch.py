import json
import os
from safety_client import SafetyClient

# Example: using Alibaba Content Moderation – provider flagged in client
CLIENT = SafetyClient()


def moderate_batch(messages: list[str]) -> list[dict]:
    """Moderate a batch of user messages and return per‑message decisions.

    Returns a list of dicts, one per input message, with the provider‑specific response.
    """
    responses = CLIENT.batch_analyze(messages)
    return responses
