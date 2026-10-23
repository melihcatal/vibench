import os
import requests
from typing import Dict

def apply_safety_threshold(text: str, thresholds: Dict[str, float]) -> bool:
    """
    Applies category thresholds to decide whether to allow text using Perspective API.
    """
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={os.getenv('PERSPECTIVE_API_KEY')}"
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
            "SEXUALLY_EXPLICIT": {}
        },
        "languages": ["en"]
    }
    response = requests.post(url, json=payload)
    result = response.json()

    for attr, score_info in result.get("attributeScores", {}).items():
        score = score_info["summaryScore"]["value"]
        if thresholds.get(attr, 0.0) < score:
            return False
    return True
