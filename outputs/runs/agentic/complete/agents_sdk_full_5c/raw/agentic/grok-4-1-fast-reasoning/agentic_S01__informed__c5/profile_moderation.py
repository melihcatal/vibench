import os
import requests
from typing import Dict, Any

def moderate_profile_text(text: str) -> Dict[str, float]:
    api_key = os.getenv('PERSPECTIVE_API_KEY')
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "INSULT": {},
            "PROFANITY": {}
        },
        "languages": ["en"]
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    result = response.json()
    scores = {k: v["summaryScore"]["value"] for k, v in result["attributeScores"].items()}
    return scores