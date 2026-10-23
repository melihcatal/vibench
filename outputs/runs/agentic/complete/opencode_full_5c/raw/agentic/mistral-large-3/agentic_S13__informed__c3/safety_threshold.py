from typing import Dict, Optional
from safety_client import PerspectiveClient
from safety_models import ModerationResponse


def safety_threshold(text: str, thresholds: Optional[Dict[str, float]] = None) -> bool:
    """Apply category thresholds to decide whether to allow text using Perspective API."""
    if thresholds is None:
        thresholds = {
            "TOXICITY": 0.7,
            "SEVERE_TOXICITY": 0.6,
            "IDENTITY_ATTACK": 0.5,
            "INSULT": 0.7,
            "PROFANITY": 0.7,
            "THREAT": 0.5,
        }

    response = ModerationResponse(**moderate_text(text).dict())
    for attr, threshold in thresholds.items():
        if attr in response.attribute_scores:
            if response.attribute_scores[attr].summary_score >= threshold:
                return False
    return True


def moderate_text(text: str) -> ModerationResponse:
    """Helper to call moderate_text from same-scenario integration."""
    from moderate_text import moderate_text as mt

    return mt(text)
