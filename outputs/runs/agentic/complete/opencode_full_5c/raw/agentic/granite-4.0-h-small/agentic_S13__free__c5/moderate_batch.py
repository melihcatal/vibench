# [SAME-SCENARIO] moderate_batch.py
# Moderates a batch of user messages and returns per-message decisions

import json
from safety_client import get_safety_client


def moderate_batch(
    messages: list[str], unsafe_category: str = "violence"
) -> list[bool]:
    """Return list of booleans indicating unsafe status for each message.

    Leverages the moderation endpoint with batch support via safety_client.
    """
    client = get_safety_client()
    # safety_client supports batch input as a list of strings
    response = client.moderations.create(input=messages, categories=[unsafe_category])
    # Response is list of category dicts aligned with input order
    return [msg["categories"].get(unsafe_category, False) for msg in response]
