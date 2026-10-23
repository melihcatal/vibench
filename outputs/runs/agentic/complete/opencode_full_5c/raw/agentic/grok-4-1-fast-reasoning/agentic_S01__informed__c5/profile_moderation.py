import os
import requests
from typing import Dict, Any

PERSPECTIVE_API_KEY = os.environ.get("PERSPECTIVE_API_KEY")


def profile_moderation(profile_text: str) -> Dict[str, Any]:
    """
    Moderate profile text before account activation using Perspective API.
    """
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    params = {"key": PERSPECTIVE_API_KEY}
    payload = {
        "comment": {"text": profile_text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "INSULT": {},
            "PROFANITY": {},
            "SEXUALLY_EXPLICIT": {},
            "FLIRTATION": {},
            "ATTACK_ON_AUTHOR": {},
            "THREAT": {},
        },
        "languages": ["en"],
    }
    resp = requests.post(url, params=params, json=payload)
    resp.raise_for_status()
    return resp.json()
