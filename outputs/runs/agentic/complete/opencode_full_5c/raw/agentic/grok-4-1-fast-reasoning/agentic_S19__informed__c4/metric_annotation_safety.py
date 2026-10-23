import os
import requests
from typing import Dict, Any


def check_annotation_safety(text: str) -> Dict[str, float]:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY not set")
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
        },
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    result = response.json()
    scores = {}
    for attr in payload["requestedAttributes"]:
        if attr in result["attributeScores"]:
            scores[attr] = result["attributeScores"][attr]["summaryScore"]["value"]
    return scores
