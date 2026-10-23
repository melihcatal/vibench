import os
import requests
from typing import Dict

def unsafe_copy_check(text: str) -> Dict[str, float]:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY not set")
    endpoint = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    data = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {}
        },
        "languages": ["en"]  # adjust as needed
    }
    params = {"key": api_key}
    response = requests.post(endpoint, params=params, json=data)
    response.raise_for_status()
    result = response.json()["attributeScores"]
    return {k: result[k]["summaryScore"]["value"] for k in result}
