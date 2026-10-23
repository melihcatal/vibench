# SAME-SCENARIO: Apply safety category thresholds

from safety_client import get_client


def apply_thresholds(text: str, thresholds: dict) -> bool:
    """Return False if any safety category exceeds its threshold.

    Uses OpenAI Moderation endpoint and respects per‑category thresholds.
    """
    client = get_client()
    response = client.moderations.create(input=text)
    for category, limit in thresholds.items():
        score = response["results"][0].get(category, 0.0)
        if score > limit:
            return False
    return True
