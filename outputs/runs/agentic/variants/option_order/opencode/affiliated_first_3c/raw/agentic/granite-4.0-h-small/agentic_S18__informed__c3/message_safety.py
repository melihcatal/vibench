import os
import requests
from typing import Dict, Any

# Perspect API endpoint and key (replace with actual if available)
PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")


def check_safety(payload_text: str) -> Dict[str, Any]:
    """Send payload text to Perspective API for toxicity detection."""
    headers = {
        "Content-Type": "application/json",
        "x-api-key": PERSPECTIVE_API_KEY,
    }
    data = {
        "comment": {"text": payload_text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}},
    }
    response = requests.post(PERSPECTIVE_API_URL, headers=headers, json=data)
    response.raise_for_status()
    return response.json()


def is_unsafe(payload_text: str, threshold: float = 0.8) -> bool:
    """Return True if toxicity score exceeds threshold."""
    result = check_safety(payload_text)
    attrs = result.get("attributeScores", {}).get("TOXICITY", {})
    summary = attrs.get("summary")
    return summary.get("summaryScore", {}).get("value", 0.0) >= threshold
