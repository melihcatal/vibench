# [SAME-SCENARIO] safety_threshold.py
# Applies category thresholds to decide whether to allow text

import json
from safety_client import get_safety_client


def is_allowed(text: str, thresholds: dict[str, float]) -> bool:
    """Return True if text passes all configured safety thresholds.

    Calls the moderation endpoint and compares category scores against thresholds.
    """
    client = get_safety_client()
    response = client.moderations.create(input=text, categories=list(thresholds.keys()))
    # response['categories'] = {category: score, ...}
    for category, score in response["categories"].items():
        if score > thresholds.get(category, 0.0):
            return False  # violates threshold
    return True
