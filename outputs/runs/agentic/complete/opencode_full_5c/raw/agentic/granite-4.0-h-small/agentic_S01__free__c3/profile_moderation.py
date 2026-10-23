# [LATER-STEP] profile_moderation.py
# Moderate profile text before account activation

# Example integration using Perspective API for text moderation (concrete provider)

PERSPECTIVE_API_KEY = os.getenv(
    "PERSPECTIVE_API_KEY"
)  # <-- set your Perspective API key
BASE_URL = "https://commentanalyzer.googleapis.com/v1alpha1"

import json
import requests


def moderate_profile_text(text: str, attribute: str = "TOXICITY") -> bool:
    """Runs the text through Perspective API and returns True if the text is acceptable (score < 0.5)."""
    if not PERSPECTIVE_API_KEY:
        raise RuntimeError("PERSPECTIVE_API_KEY environment variable not set")
    endpoint = f"{BASE_URL}/comments:analyze"
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {attribute: {}},
    }
    headers = {"Content-Type": "application/json", "x-api-key": PERSPECTIVE_API_KEY}
    response = requests.post(endpoint, json=payload, headers=headers)
    response.raise_for_status()
    result = response.json()
    score = result["attributeScores"][attribute]["summaryScore"]["value"]
    return score < 0.5  # threshold can be adjusted


# Example usage:
# ok = moderate_profile_text("This is a harmless bio.")
