# SAME-SCENARIO: moderate_batch.py
"""Moderate a batch of user messages and return per‑message moderation results."""

import os
from typing import List, Dict
from safety_client import get_moderation_client

API_MODEL = "openai.moderation"  # concrete provider identifier


def moderate_batch(messages: List[str], threshold: float = 0.5) -> List[Dict]:
    """Return a list containing moderation result dicts for each message.

    Args:
        messages: A list of strings to evaluate.
        threshold: Score above which content is considered unsafe.

    Returns:
        A list where each element is the normalized dict from moderate_text.
    """
    client = get_moderation_client()
    raw = client.moderate(
        model=API_MODEL,
        batch=True,
        **{f"message_{i}": msg for i, msg in enumerate(messages)},
    )
    results = []
    for i, res in enumerate(raw["results"]):
        results.append(
            {
                "message_id": i,
                "raw": res,
                "safe": not any(hit["flagged"] for hit in res["categories"]),
            }
        )
    return results
