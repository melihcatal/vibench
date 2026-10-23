# [SAME-SCENARIO] safety_threshold.py
"""Applies category thresholds to decide whether to allow text using OpenAI Moderation API."""

from safety_client import get_openai_client


def allow_by_threshold(text: str, thresholds: dict) -> bool:
    """Return True if all flagged categories are below their allowed thresholds."""
    client = get_openai_client()
    response = client.moderations.create(input=text)
    results = response["results"][0]
    for category, limit in thresholds.items():
        # Assume response includes a count/confidence per category
        if category in results["categories"]:
            score = results["categories"][category]
            if score > limit:
                return False
    return True
