import os
import requests
from typing import List, Dict

PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")

def moderate_claims(claims: List[str]) -> List[Dict[str, float]]:
    results = []
    for claim in claims:
        payload = {
            "comment": {"text": claim},
            "requestedAttributes": {
                "TOXICITY": {},
                "SEVERE_TOXICITY": {},
                "INSULT": {},
                "PROFANITY": {},
                "IDENTITY_ATTACK": {},
            },
            "languages": ["en", "und"],
        }
        resp = requests.post(f"{PERSPECTIVE_API_URL}?key={PERSPECTIVE_API_KEY}", json=payload)
        resp.raise_for_status()
        scores = resp.json().get("attributeScores", {})
        score_dict = {
            attr: scores.get(attr, {}).get("summaryScore", {}).get("value", 0.0)
            for attr in ["TOXICITY", "SEVERE_TOXICITY", "INSULT", "PROFANITY", "IDENTITY_ATTACK"]
        }
        results.append(score_dict)
    return results