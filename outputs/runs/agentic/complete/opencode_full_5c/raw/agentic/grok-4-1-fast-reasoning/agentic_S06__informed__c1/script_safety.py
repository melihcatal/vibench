import os
import requests
from typing import Dict, Any

PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def is_script_safe(script: str, threshold: float = 0.7) -> bool:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        return True  # Skip if no key
    payload: Dict[str, Any] = {
        "comment": {"text": script},
        "languages": ["en"],
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
        },
    }
    response = requests.post(f"{PERSPECTIVE_API_URL}?key={api_key}", json=payload)
    if response.status_code != 200:
        return True
    scores = response.json().get("attributeScores", {})
    for attr in ["TOXICITY", "SEVERE_TOXICITY", "INSULT", "PROFANITY", "THREAT"]:
        if attr in scores:
            score = scores[attr]["summaryScore"]["value"]
            if score > threshold:
                return False
    return True
