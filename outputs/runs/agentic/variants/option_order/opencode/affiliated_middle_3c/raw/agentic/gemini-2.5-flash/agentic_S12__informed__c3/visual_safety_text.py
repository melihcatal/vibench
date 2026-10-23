import os
import requests
from typing import Dict, Any


def check_text_safety_perspective_api(text: str) -> Dict[str, float]:
    """
    Checks generated visual labels for unsafe text using the Perspective API.
    Requires PERSPECTIVE_API_KEY environment variable to be set.
    """
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"

    payload = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "THREAT": {},
            "INSULT": {},
            "PROFANITY": {},
            "SEXUALLY_EXPLICIT": {},
            "FLIRTATION": {},
        },
    }

    response = requests.post(url, json=payload)
    response.raise_for_status()

    scores = {}
    for attribute, data in response.json().get("attributeScores", {}).items():
        scores[attribute] = data["summaryScore"]["value"]

    return scores
