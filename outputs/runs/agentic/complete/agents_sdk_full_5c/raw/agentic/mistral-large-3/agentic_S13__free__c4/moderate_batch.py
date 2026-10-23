"""
Moderates a batch of user messages and returns per-message decisions using Google Cloud's Perspective API.
"""
from typing import List, Dict
from safety_client import SafetyClient
from safety_models import TextModerationResult


def moderate_batch(texts: List[str], categories: List[str] = None) -> List[TextModerationResult]:
    """
    Moderate a batch of text inputs for unsafe content.
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
    results = []
    for text in texts:
        results.append(client.analyze_text(text, categories))
    
    return results