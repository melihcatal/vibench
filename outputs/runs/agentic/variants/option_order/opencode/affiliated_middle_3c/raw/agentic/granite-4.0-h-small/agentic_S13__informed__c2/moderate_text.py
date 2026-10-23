import os
import requests

# Perspective API integration
API_ENDPOINT = "https://commentanalyzer.googleapis.com/v1/analyze"
API_KEY = os.getenv("PERSPECTIVE_API_KEY")


def moderate_text(user_text: str) -> dict:
    """Score user text for unsafe or policy-violating content using Perspective API.

    Returns a dict with the original text and the scores returned by the API.
    """
    headers = {
        "X-API-KEY": API_KEY,
        "Content-Type": "application/json",
    }  # Perspective expects X-API-KEY
    payload = {
        "comment": {"text": user_text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_HATE": {},
        },
    }
    response = requests.post(API_ENDPOINT, json=payload, headers=headers)
    response.raise_for_status()
    result = response.json()
    return {"text": user_text, "scores": result.get("attributeScores", {})}
