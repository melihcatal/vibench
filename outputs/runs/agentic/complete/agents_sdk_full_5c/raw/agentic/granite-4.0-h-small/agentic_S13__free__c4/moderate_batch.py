# moderate_batch.py
"""Moderates a batch of user messages and returns per-message decisions.
"""
import os
from safety_client import OpenAIContentSafetyClient

def moderate_batch(messages: list[str]) -> list[dict]:
    """Return a list of moderation decisions corresponding to each message.
    Each decision dict follows the shape defined in moderate_text.py."""
    client = OpenAIContentSafetyClient()
    response = client.moderate(messages)
    output = []
    for result in response:
        r = result["results"][0]
        output.append({
            "passed": not r["flagged"],
            "flagged_categories": r["flagged_categories"],
            "detail": r.get("detail")
        })
    return output
