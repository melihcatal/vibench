import requests
import os
from typing import Dict, Any

def check_content_safety(text: str, client_id: str = "default-client") -> Dict[str, Any]:
    """
    Checks prompts and generated text for unsafe content using Perspective API.
    Expects PERSPECTIVE_API_KEY environment variable to be set.
    """
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    params = {
        "key": api_key
    }
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
        "clientToken": client_id
    }
    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, params=params, json=data, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error checking content safety with Perspective API: {e}")
        return {"error": str(e)}
