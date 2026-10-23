"""
Applies category thresholds to decide whether to allow text using Google Cloud's Perspective API.
"""
from typing import List, Dict
from safety_client import SafetyClient
from safety_models import TextModerationResult


def apply_safety_threshold(
    text: str,
    thresholds: Dict[str, float],
    categories: List[str] = None
) -> bool:
    """
    Apply category thresholds to decide if text is allowed.
    Returns True if all category scores are below thresholds, False otherwise.
    Default categories: TOXICITY, SEVERE_TOXICITY, IDENTITY_ATTACK, INSULT, PROFANITY, THREAT.
    """
    if categories is None:
        categories = [
            "TOXICITY",
            "SEVERE_TOXICITY",
            "IDENTITY_ATTACK",
            "INSULT",
            "PROFANITY",
            "THREAT"
        ]
    
    client = SafetyClient()
    result = client.analyze_text(text, categories)
    
    for score in result.scores:
        if score.category in thresholds and score.score >= thresholds[score.category]:
            return False
    
    return True