import os
import requests
from typing import Dict


def check_platform_output_safety(text: str) -> Dict[str, float]:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    payload = {
        "comment": {"text": text[:20000]},
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
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    scores = response.json()["attributeScores"]
    return {attr: scores[attr]["summaryScore"]["value"] for attr in scores}
