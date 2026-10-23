# [LATER-STEP] profile_moderation.py
# Moderate profile text before account activation using Perspective API
import os
import requests
import json

# Provider identification: Google Perspective API
PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")
BASE_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

MAX_TOXICITY_SCORE = 0.7  # configurable threshold


def moderate_profile(profile_text: str) -> bool:
    """Return True if profile text passes moderation, else False."""
    payload = {
        "comment": {"text": profile_text},
        "requestedAttributes": {"TOXICITY": {}},
    }
    headers = {"key": PERSPECTIVE_API_KEY, "contentType": "application/json"}
    resp = requests.post(BASE_URL, json=payload, headers=headers)
    resp.raise_for_status()
    result = resp.json()["attributeScores"]["TOXICITY"]["summaryScore"]
    toxicity = result["value"]
    return toxicity <= MAX_TOXICITY_SCORE
