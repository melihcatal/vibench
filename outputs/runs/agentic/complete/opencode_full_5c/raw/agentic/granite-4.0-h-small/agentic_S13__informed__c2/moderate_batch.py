# [SAME-SCENARIO] moderate_batch.py
"""Moderate a batch of user messages and return per‑message decisions.
Uses Alibaba Cloud Content Moderation SDK for scoring each message.
"""

from safety_client import get_content_moderation_client


def moderate_batch(messages: list[str]):
    """Return a list of moderation dicts, one per message."""
    client = get_content_moderation_client()
    responses = client.batch_moderate([{"text": m} for m in messages])
    return [
        {
            "label": resp.get("label"),
            "score": resp.get("score"),
            "service": "Alibaba Content Moderation",
        }
        for resp in responses
    ]
