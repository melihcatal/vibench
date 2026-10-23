import requests
import os
from typing import List, Dict


def check_secret_labels_safety(labels_notes: List[str]) -> List[Dict]:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    results = []
    for text in labels_notes:
        if not text.strip():
            results.append({})
            continue
        data = {
            "comment": {"text": text},
            "languages": ["en"],
            "requestedAttributes": {
                "TOXICITY": {},
                "SEVERE_TOXICITY": {},
                "INSULT": {},
                "PROFANE": {},
                "IDENTITY_ATTACK": {},
                "THREAT": {},
            },
        }
        resp = requests.post(
            f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}",
            json=data,
        )
        resp.raise_for_status()
        scores = resp.json().get("attributeScores", {})
        results.append({k: v["summaryScore"]["value"] for k, v in scores.items()})
    return results
