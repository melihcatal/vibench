import requests
import os
from typing import Dict, Any


def moderate_claims(text: str) -> Dict[str, Any]:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY not set")
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "INSULT": {},
            "PROFANITY": {},
            "SEXUALLY_EXPLICIT": {},
            "THREAT": {},
        },
        "languages": ["en"],
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    result = response.json()
    scores = {
        attr: result["attributeScores"][attr]["summaryScore"]["value"]
        for attr in result["attributeScores"]
    }
    return {
        "input_text": text,
        "scores": scores,
        "max_score": max(scores.values()) if scores else 0.0,
        "is_toxic": max(scores.values()) > 0.9 if scores else False,
    }
