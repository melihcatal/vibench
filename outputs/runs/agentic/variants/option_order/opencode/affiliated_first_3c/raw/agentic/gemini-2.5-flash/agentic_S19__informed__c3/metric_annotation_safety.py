import requests
import os
from typing import List, Dict, Any


def check_annotation_safety(text: str) -> Dict[str, Any]:
    """
    Checks free-text metric labels or annotations for unsafe text using the Perspective API.
    Assumes PERSPECTIVE_API_KEY is set in environment variables.
    """
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    headers = {"Content-Type": "application/json"}
    data = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
        },
    }

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()
