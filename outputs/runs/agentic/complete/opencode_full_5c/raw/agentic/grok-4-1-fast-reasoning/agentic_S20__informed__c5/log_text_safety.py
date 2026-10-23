import os
import requests
from typing import Dict, Any


def check_log_safety(log_message: str) -> Dict[str, Dict[str, Any]]:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    payload = {
        "comment": {"text": log_message},
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
    scores = response.json().get("attributeScores", {})
    return scores
