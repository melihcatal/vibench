import os
import requests
from typing import Dict, Any

# Google Perspective API provider
PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")

def log_text_safety(text: str) -> Dict[str, float]:
    """
    Check selected log message text for unsafe content using Google Perspective API.
    """
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={PERSPECTIVE_API_KEY}"
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {}
        },
        "languages": ["en"]
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    result = response.json()
    scores = {
        attr: data["summaryScore"]["value"]
        for attr, data in result["attributeScores"].items()
    }
    return scores