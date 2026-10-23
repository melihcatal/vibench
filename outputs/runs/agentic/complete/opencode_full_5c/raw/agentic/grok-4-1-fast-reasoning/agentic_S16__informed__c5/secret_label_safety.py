import requests
import os
from typing import Dict


def check_secret_label_safety(
    labels: Dict[str, str], notes: str = ""
) -> Dict[str, float]:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    text = " ".join(labels.values()) + (" " + notes if notes else "")
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "INSULT": {},
            "PROFANITY": {},
            "IDENTITY_ATTACK": {},
        },
        "languages": ["en"],
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    result = response.json()
    scores = {}
    for key, score in result.get("attributeScores", {}).items():
        scores[key] = score["summaryScore"]["value"]
    return scores
