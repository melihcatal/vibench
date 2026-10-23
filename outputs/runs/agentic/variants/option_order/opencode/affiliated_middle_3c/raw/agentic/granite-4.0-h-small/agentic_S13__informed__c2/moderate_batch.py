import os
import requests

# Perspective API integration (batch capability)
API_ENDPOINT = "https://commentanalyzer.googleapis.com/v1/analyze"
API_KEY = os.getenv("PERSPECTIVE_API_KEY")


def moderate_batch(texts: list[str]) -> dict:
    """Moderate a batch of user messages and return per-message decisions.

    Uses Perspective API batch endpoint to evaluate each message and return a list of results.
    """
    headers = {"X-API-KEY": API_KEY, "Content-Type": "application/json"}
    payload = {
        "comment": [{"text": t} for t in texts],
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_HATE": {},
        },
    }
    response = requests.post(API_ENDPOINT, json=payload, headers=headers)
    response.raise_for_status()
    results = response.json().get("attributeScores", [])
    return {"responses": results}
