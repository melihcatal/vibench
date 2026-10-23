import os
import requests
from typing import Dict, Any

PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")
if not PERSPECTIVE_API_KEY:
    raise ValueError("PERSPECTIVE_API_KEY must be set.")

ATTRIBUTES = [
    "TOXICITY", "SEVERE_TOXICITY", "INSULT", "PROFANITY",
    "SEXUALLY_EXPLICIT", "FLIRTATION", "HATE_SPEECH"
]

def check_safety(text: str) -> Dict[str, float]:
    """Check text for unsafe content using Perspective API."""
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={PERSPECTIVE_API_KEY}"
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {attr: {} for attr in ATTRIBUTES}
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    result = response.json()
    scores = {
        attr: result["attributeScores"][attr]["summaryScore"]["value"]
        for attr in ATTRIBUTES
    }
    return scores

def is_unsafe(text: str, threshold: float = 0.7) -> bool:
    """Return True if text is unsafe."""
    scores = check_safety(text)
    return max(scores.values()) > threshold