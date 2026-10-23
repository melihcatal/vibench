import os
import requests

# Perspective API integration
API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")

def moderate_text(user_text: str, threshold: float = 0.5) -> dict:
    """Score user text for unsafe content using Perspective API.

    Returns a dict with the original text, a safety score for the TOXICITY attribute,
    and a boolean indicating whether the content exceeds the threshold.
    """
    payload = {
        "comment": {
            "text": user_text,
            "type": "PLAIN_TEXT"
        },
        "requestedAttributes": {
            "TOXICITY": {}
        }
    }
    headers = {
        "content-type": "application/json",
        "x-goog-api-key": PERSPECTIVE_API_KEY
    }
    response = requests.post(API_URL, json=payload, headers=headers)
    response.raise_for_status()
    result = response.json()
    score = result["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
    return {
        "text": user_text,
        "toxicity_score": score,
        "exceeds_threshold": score >= threshold
    }
