import requests
import os
from typing import Dict, Any

# Perspective API endpoint and API key
PERSPECTIVE_API_BASE_URL = (
    "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
)
PERSPECTIVE_API_KEY = os.environ.get("PERSPECTIVE_API_KEY")


def check_text_safety(text: str) -> Dict[str, Any]:
    if not PERSPECTIVE_API_KEY:
        return {
            "status": "error",
            "message": "PERSPECTIVE_API_KEY environment variable not set.",
        }

    url = f"{PERSPECTIVE_API_BASE_URL}?key={PERSPECTIVE_API_KEY}"

    headers = {"Content-Type": "application/json"}
    payload = {
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

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"status": "error", "message": f"Perspective API request failed: {e}"}
