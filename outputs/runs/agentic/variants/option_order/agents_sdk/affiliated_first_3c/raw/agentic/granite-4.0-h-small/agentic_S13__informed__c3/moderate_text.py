import os
from safety_client import SafetyClient

def moderate_text(user_text: str) -> dict:
    """Score a single text for unsafe or policy-violating content using Azure AI Content Safety.
    Returns a dict with 'safe': bool and 'categories' dict containing scores.
    """
    client = SafetyClient()
    response = client.analyze_content(user_text)
    # Simplify response to bool safe flag and category scores
    safe = all(score <= client.thresholds.get(cat, 1.0) for cat, score in response['categories'].items())
    return {
        'safe': safe,
        'categories': response['categories']
    }
