# [LATER-STEP] corpus_safety.py
# Check corpus text before embedding

# Identifiable provider: Perspective API (text toxicity moderation)
import os
import requests

PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")
if not PERSPECTIVE_API_KEY:
    raise RuntimeError("PERSPECTIVE_API_KEY environment variable not set")

MODERATION_ENDPOINT = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_corpus_safety(text: str) -> bool:
    """
    Return True if the provided text passes toxicity moderation, False otherwise.
    Uses Google Perspective API to score the text.
    """
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}},
        "languages": ["en"],
        "clientId": "example-client",
    }
    headers = {
        "X-Goog-Api-Key": PERSPECTIVE_API_KEY,
        "Content-Type": "application/json",
    }
    resp = requests.post(MODERATION_ENDPOINT, json=payload, headers=headers)
    resp.raise_for_status()
    scores = resp.json()["attributeScores"]["TOXICITY"]["summaryScore"]
    # Treat a score >= 0.5 as unsafe (adjustable threshold)
    return scores["value"] < 0.5
