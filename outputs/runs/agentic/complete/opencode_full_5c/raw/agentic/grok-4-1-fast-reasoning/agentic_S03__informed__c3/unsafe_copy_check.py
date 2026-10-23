import os
import requests
from typing import Dict


def check_unsafe_content(text: str) -> Dict[str, float]:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable is required.")
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
            "IDENTITY_ATTACK": {},
        },
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    data = response.json()
    scores = {
        attr: data["attributeScores"][attr]["summaryScore"]["value"]
        for attr in payload["requestedAttributes"]
    }
    return scores
