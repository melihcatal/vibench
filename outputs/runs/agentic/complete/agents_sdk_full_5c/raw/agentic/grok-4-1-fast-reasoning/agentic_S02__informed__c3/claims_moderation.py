import os
import requests
from typing import List, Dict, Any

PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")

def moderate_claims(claims: List[str]) -> List[Dict[str, Any]]:
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    results = []
    for claim in claims:
        data = {
            "comment": {"text": claim},
            "languages": ["en"],
            "requestedAttributes": {
                "TOXICITY": {},
                "SEVERE_TOXICITY": {},
                "INSULT": {},
                "PROFANITY": {},
                "IDENTITY_ATTACK": {},
            },
        }
        resp = requests.post(f"{url}?key={PERSPECTIVE_API_KEY}", json=data)
        resp.raise_for_status()
        scores = resp.json().get("attributeScores", {})
        result = {
            "claim": claim,
            "scores": {k: v["summaryScore"]["value"] for k, v in scores.items()}
        }
        results.append(result)
    return results