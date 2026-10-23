"""
Scores user text for unsafe or policy-violating content using Google Cloud's Perspective API.
"""
from typing import List
from safety_client import SafetyClient
from safety_models import TextModerationResult


def moderate_text(text: str, categories: List[str] = None) -> TextModerationResult:
    """
    Moderate a single text input for unsafe content.
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
    return client.analyze_text(text, categories)