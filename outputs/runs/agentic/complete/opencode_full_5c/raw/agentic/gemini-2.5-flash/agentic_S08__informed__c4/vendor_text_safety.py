import os
import requests
from typing import Dict, Any


def moderate_vendor_notes(text_to_moderate: str) -> Dict[str, Any]:
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError(
            "Perspective API key not set in environment variable PERSPECTIVE_API_KEY."
        )

    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    headers = {"Content-Type": "application/json"}
    data = {
        "comment": {"text": text_to_moderate},
        "requestedAttributes": {"TOXICITY": {}},
    }

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()  # Raise an exception for HTTP errors

    return response.json()
