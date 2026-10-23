# profile_moderation.py
# Moderate profile text before account activation (Perspective API reference)

import os
import json
import requests
from typing import Dict, Any
from identity_models import normalize_user_profile

# Perspective API key (set as environment variable)
PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")
if not PERSPECTIVE_API_KEY:
    raise RuntimeError("Set PERSPECTIVE_API_KEY environment variable")

PERSPECTIVE_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def moderate_profile(profile: Dict[str, Any], text: str) -> Dict[str, Any]:
    """Run content moderation on profile text and return a safe version."""
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}, "SEVERE_TOXICITY": {}},
    }
    headers = {
        "key": PERSPECTIVE_API_KEY,
        "content-type": "application/json",
    }
    resp = requests.post(PERSPECTIVE_URL, json=payload, headers=headers)
    resp.raise_for_status()
    scores = resp.json()["attributeScores"]
    # If severe toxicity > 0.8, replace with moderated version
    if scores.get("SEVERE_TOXICITY", {}).get("summaryScore", {}).get("value", 0) > 0.8:
        moderated = "We've removed inappropriate content from your profile for safety."
    else:
        moderated = text  # keep original
    profile["moderated_profile"] = moderated
    return profile


# Example usage (do not run in production script)
if __name__ == "__main__":
    raw_profile = {
        "user_id": "123",
        "email": "bob@example.com",
        "status": "pending",
    }
    user_text = "This is a test profile with some rude language!!!"
    safe_profile = moderate_profile(raw_profile, user_text)
    print(json.dumps(safe_profile, indent=2))
