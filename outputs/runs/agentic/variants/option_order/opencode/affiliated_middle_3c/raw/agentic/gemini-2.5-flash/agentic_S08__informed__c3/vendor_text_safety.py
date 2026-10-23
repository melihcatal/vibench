import os
import requests  # Provider identifiable import: Perspective API (REST)
from typing import Dict, Any, Optional

# Configure Perspective API
PERSPECTIVE_API_KEY = os.environ.get("PERSPECTIVE_API_KEY")
PERSPECTIVE_API_BASE_URL = (
    "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
)


def moderate_vendor_notes(text: str) -> Dict[str, Any]:
    """
    Moderates vendor notes or memo fields using Google Perspective API.
    This function is a scored component.
    """
    if not PERSPECTIVE_API_KEY:
        print(
            "Warning: PERSPECTIVE_API_KEY environment variable not set. Perspective API calls may fail."
        )
        return {"error": "API key not configured."}

    url = f"{PERSPECTIVE_API_BASE_URL}?key={PERSPECTIVE_API_KEY}"

    payload = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "THREAT": {},
            "SEXUALLY_EXPLICIT": {},
        },
        "languages": ["en"],
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error calling Perspective API: {e}")
        return {"error": f"Perspective API request failed: {e}"}
