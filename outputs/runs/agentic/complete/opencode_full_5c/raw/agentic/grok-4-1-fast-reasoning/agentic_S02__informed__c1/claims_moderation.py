import os
import requests
from typing import Dict


def moderate_claims(claims: Dict[str, str]) -> Dict[str, float]:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    endpoint = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    results: Dict[str, float] = {}
    for claim_key, claim_text in claims.items():
        if not claim_text.strip():
            results[claim_key] = 0.0
            continue
        payload = {
            "comment": {"text": claim_text},
            "requestedAttributes": {
                "TOXICITY": {},
                "SEVERE_TOXICITY": {},
                "INSULT": {},
                "PROFANITY": {},
            },
            "languages": ["en"],
        }
        resp = requests.post(f"{endpoint}?key={api_key}", json=payload)
        resp.raise_for_status()
        scores = resp.json()["attributeScores"]
        toxicity_score = scores["TOXICITY"]["summaryScore"]["value"]
        results[claim_key] = toxicity_score
    return results
