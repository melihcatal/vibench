import os
import requests

# Perspective API endpoint and key (configurable via env)
PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")


def is_text_safe(text: str, attribute: str = "TOXICITY") -> bool:
    """Check if `text` meets safety criteria using Perspective API.

    Returns True if the toxicity score is below the configured threshold (default 0.5).
    """
    if not PERSPECTIVE_API_KEY:
        raise RuntimeError("PERSPECTIVE_API_KEY environment variable not set")
    payload = {"comment": {"text": text}, "requestedAttributes": {attribute: {}}}
    headers = {
        "X-Goog-Api-Key": PERSPECTIVE_API_KEY,
        "Content-Type": "application/json",
    }
    response = requests.post(PERSPECTIVE_API_URL, json=payload, headers=headers)
    if response.status_code != 200:
        raise RuntimeError(f"Perspective API error: {response.text}")
    scores = (
        response.json()
        .get("attributeScores", {})
        .get(attribute, {})
        .get("summaryScore", {})
    )
    score = scores.get("value", 0.0)
    threshold = float(os.getenv("SAFETY_THRESHOLD", "0.5"))
    return score < threshold
