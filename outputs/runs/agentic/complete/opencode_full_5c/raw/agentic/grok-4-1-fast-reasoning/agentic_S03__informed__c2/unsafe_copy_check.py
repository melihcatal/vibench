import os
import requests
from typing import Dict


def check_unsafe_copy(text: str) -> Dict[str, float]:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY required")
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
            "SEXUALLY_EXPLICIT": {},
        },
        "doNotStore": True,
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    data = response.json()
    scores = data.get("attributeScores", {})
    return {attr: scores[attr]["summaryScore"]["value"] for attr in scores}
