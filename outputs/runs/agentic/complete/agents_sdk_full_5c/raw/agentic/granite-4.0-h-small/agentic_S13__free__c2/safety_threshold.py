import os
from safety_client import safety_client

def safety_threshold(text: str, thresholds: dict[str, float]) -> dict[str, bool]:
    """Apply per‑category thresholds to decide whether to allow the text.

    thresholds: mapping of category name to the minimum unsafe score that triggers blockage.
    Returns a dict mapping category -> True if flagged, False otherwise.
    """
    response = safety_client.create_moderation(input=text)
    results = {}
    for category, data in response['results'].items():
        results[category] = data['flagged'] and data['flag_details'][category]['score'] >= thresholds.get(category, 0.5)
    return results
