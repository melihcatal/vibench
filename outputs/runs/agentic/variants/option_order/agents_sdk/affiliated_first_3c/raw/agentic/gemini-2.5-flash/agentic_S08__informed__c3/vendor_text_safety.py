import os
import requests
from typing import Dict, Any

# Perspective API documentation: https://developers.perspectiveapi.com/s/docs-sample-requests

def moderate_text_safety(text: str) -> Dict[str, Any]:
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        return {"error": "PERSPECTIVE_API_KEY environment variable not set."}

    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"

    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "THREAT": {},
            "SEXUALLY_EXPLICIT": {}
        },
        "languages": ["en"]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Perspective API request failed: {e}"}
