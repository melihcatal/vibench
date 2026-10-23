import os
import requests
from typing import List, Dict, Any

def moderate_claims(claims: List[str]) -> List[Dict[str, Any]]:
    api_key = os.getenv('PERSPECTIVE_API_KEY')
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY not set")
    endpoint = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    url = f"{endpoint}?key={api_key}"
    results = []
    for claim in claims:
        payload = {
            "comment": {"text": claim},
            "languages": ["en"],
            "requestedAttributes": {
                "TOXICITY": {},
                "SEVERE_TOXICITY": {},
                "INSULT": {},
                "PROFANITY": {},
                "IDENTITY_ATTACK": {}
            },
            "doNotStore": True
        }
        resp = requests.post(url, json=payload)
        resp.raise_for_status()
        attribute_scores = resp.json().get('attributeScores', {})
        results.append({
            "claim": claim,
            "scores": {k: v['summaryScore']['value'] for k, v in attribute_scores.items()}
        })
    return results
