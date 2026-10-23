import os
import requests
from typing import Dict


def analyze_safety(script: str) -> Dict[str, float]:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    payload = {
        "comment": {"text": script},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "INSULT": {},
            "PROFANE": {},
            "IDENTITY_ATTACK": {},
            "THREAT": {},
        },
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    scores = response.json()["attributeScores"]
    return {attr: scores[attr]["summaryScore"]["value"] for attr in scores}


def is_safe(script: str, max_toxicity: float = 0.3) -> bool:
    scores = analyze_safety(script)
    return all(score < max_toxicity for score in scores.values())
