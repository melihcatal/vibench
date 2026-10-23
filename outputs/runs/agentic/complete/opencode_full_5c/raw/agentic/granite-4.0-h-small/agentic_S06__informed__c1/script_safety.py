# script_safety.py
import os
import requests

PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

API_KEY = os.getenv("PERSPECTIVE_API_KEY")

if not API_KEY:
    raise RuntimeError("Set PERSPECTIVE_API_KEY environment variable")


def is_unsafe(script):
    """Return True if the script contains unsafe content according to Perspective API."""
    payload = {
        "comment": {"text": script},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}, "SEVERE_TOXICITY": {}},
    }
    headers = {"x-api-key": API_KEY}
    response = requests.post(PERSPECTIVE_API_URL, json=payload, headers=headers)
    resp_json = response.json()
    # Simple heuristic: if any attribute score > 0.8, consider unsafe
    for attr, data in resp_json.get("attributeScores", {}).items():
        if data.get("summaryScore", {}).get("value", 0) > 0.8:
            return True
    return False
