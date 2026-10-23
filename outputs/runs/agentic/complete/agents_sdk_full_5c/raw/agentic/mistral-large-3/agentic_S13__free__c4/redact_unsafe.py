"""
Flags or redacts unsafe spans from text using Google Cloud's Perspective API.
"""
from typing import List
from safety_client import SafetyClient
from safety_models import TextRedactionResult


def redact_unsafe(text: str, categories: List[str] = None, threshold: float = 0.7) -> TextRedactionResult:
    """
    Redact unsafe spans from text based on Perspective API scores.
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
    return client.redact_unsafe_spans(text, categories, threshold)