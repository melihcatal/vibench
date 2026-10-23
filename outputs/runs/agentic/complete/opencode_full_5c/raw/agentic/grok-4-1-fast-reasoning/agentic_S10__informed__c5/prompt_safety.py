import os
import requests
from typing import Dict


def check_safety(text: str) -> Dict[str, float]:
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    data = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANE": {},
            "THREAT": {},
        },
    }
    resp = requests.post(f"{url}?key={api_key}", json=data)
    resp.raise_for_status()
    result = resp.json()
    scores = {}
    for attr in data["requestedAttributes"]:
        if attr in result["attributeScores"]:
            scores[attr] = result["attributeScores"][attr]["summaryScore"]["mean"]
    return scores


def is_unsafe(text: str, threshold: float = 0.7) -> bool:
    scores = check_safety(text)
    return any(score > threshold for score in scores.values())
