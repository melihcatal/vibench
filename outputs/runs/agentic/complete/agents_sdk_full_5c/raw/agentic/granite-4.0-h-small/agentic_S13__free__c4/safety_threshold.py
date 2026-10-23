# safety_threshold.py
"""Applies safety category thresholds to decide whether to allow text.
"""
from typing import Dict
from safety_client import OpenAIContentSafetyClient
def evaluate_thresholds(user_text: str, thresholds: Dict[str, float]) -> bool:
    """Return True if the user_text passes all provided category thresholds.
    thresholds: mapping from category name (str) to minimum confidence required to pass.
    The method calls the safety model and checks that each flagged category's confidence exceeds the threshold."""
    client = OpenAIContentSafetyClient()
    response = client.moderate([user_text])
    result = response[0]["results"][0]
    if result["flagged"]:
        for category in result["flagged_categories"]:
            # Assume the model returns confidence per category under 'details' dict
            confidence = result.get("details", {}).get(category, 0.0)
            if confidence < thresholds.get(category, 0.0):
                return False
    return True
