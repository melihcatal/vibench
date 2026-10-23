import os
import requests
from typing import Dict, Any


def check_corpus_safety(text: str) -> Dict[str, Any]:
    """Checks the safety of corpus text using Google's Perspective API."""
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "THREAT": {},
            "SEXUALLY_EXPLICIT": {},
            "FLIRTATION": {},
            "SPAM": {},
            "ATTACK_ON_AUTHOR": {},
            "ATTACK_ON_OTHER_TOPIC": {},
        },
        "languages": ["en"],
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error checking corpus safety with Perspective API: {e}")
        return {"error": str(e)}
