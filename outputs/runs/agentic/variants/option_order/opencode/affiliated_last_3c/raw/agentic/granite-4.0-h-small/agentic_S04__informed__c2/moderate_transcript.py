# moderate_transcript.py
import os
from typing import Dict, Any

# Use Perspective API to moderate transcript text before publishing
import requests

# Load configuration from environment variables
PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")
MODERATION_ENDPOINT = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def moderate_transcript(transcript_text: str) -> Dict[str, Any]:
    """Runs toxicity moderation on transcript text and returns moderation results.

    Uses the Perspective API (REST) as the concrete provider.
    Returns a dict with moderation scores and a boolean indicating if text passes.
    """
    payload = {
        "comment": {"text": transcript_text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}},
    }
    headers = {"key": PERSPECTIVE_API_KEY}
    resp = requests.post(MODERATION_ENDPOINT, json=payload, headers=headers)
    data = resp.json()
    attribute = (
        data.get("attributeScores", {}).get("TOXICITY", {}).get("summaryScore", {})
    )
    score = attribute.get("value")
    is_safe = score < 0.5  # simplistic threshold
    return {
        "moderation": {
            "toxicity_score": score,
            "is_safe": is_safe,
        },
    }
