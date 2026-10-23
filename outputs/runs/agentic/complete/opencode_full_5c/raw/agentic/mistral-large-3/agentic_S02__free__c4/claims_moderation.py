import requests
import os
from typing import Dict, Any

# Perspective API Configuration (Google)
PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY", "your-perspective-api-key")
PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def moderate_claims(text: str) -> Dict[str, Any]:
    """Moderate free-text claims using Google's Perspective API."""
    params = {"key": PERSPECTIVE_API_KEY}
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
        },
        "languages": ["en"],
    }
    response = requests.post(PERSPECTIVE_API_URL, params=params, json=payload)
    response.raise_for_status()
    return response.json()


def is_claim_acceptable(
    moderation_result: Dict[str, Any], threshold: float = 0.7
) -> bool:
    """Determine if a claim is acceptable based on Perspective API results."""
    attributes = moderation_result.get("attributeScores", {})
    for attribute in attributes.values():
        if attribute["summaryScore"]["value"] > threshold:
            return False
    return True
