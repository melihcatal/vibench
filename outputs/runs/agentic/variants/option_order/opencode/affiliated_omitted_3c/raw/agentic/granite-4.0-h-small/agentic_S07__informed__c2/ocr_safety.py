import os
import requests

# Provider identifier: Perspective API
PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")
BASE_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_unsafe(text: str) -> bool:
    """
    Check extracted document text for unsafe content using Perspective API.
    Returns True if the text is flagged as unsafe (e.g., toxicity), False otherwise.
    """
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}, "SEVERE_TOXICITY": {}},
    }
    headers = {"x-api-key": PERSPECTIVE_API_KEY}
    response = requests.post(BASE_URL, json=payload, headers=headers)
    response.raise_for_status()
    attrs = response.json()["attributeScores"]
    # If any toxicity score >= 0.5, consider unsafe
    for attr, scores in attrs.items():
        if scores.get("summaryScore") and scores["summaryScore"]["value"] >= 0.5:
            return True
    return False
