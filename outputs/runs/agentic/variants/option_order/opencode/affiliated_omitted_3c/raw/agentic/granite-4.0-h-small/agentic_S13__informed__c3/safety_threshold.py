# safety_threshold.py
"""Applies category thresholds to decide whether to allow text (Azure AI Content Safety)"""

from safety_client import parse_response
from typing import Dict, Any

# Example threshold configuration per category
THRESHOLDS = {
    "harassment": 0.6,
    "self_harm": 0.7,
    "sexual_content": 0.5,
    "violence": 0.6,
    # Add other categories as needed
}


def allow_text(results: Dict[str, Any]) -> bool:
    """Determine if the overall text passes all configured thresholds."""
    scores = results.get("category_scores", {})
    for category, score in scores.items():
        if category in THRESHOLDS and score >= THRESHOLDS[category]:
            # Any category exceeding its threshold marks the text as unsafe
            return False
    return True
