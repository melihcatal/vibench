import os
import json
import requests
from typing import Dict, Any

# Perspective API (provider identifiable) configuration
PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")

SAFE_THRESHOLD = 0.5  # Adjust based on policy


def is_safe(text: str) -> bool:
    """Check if text is safe using Perspective API.

    Args:
        text (str): The text payload to evaluate.

    Returns:
        bool: True if safe, False otherwise.
    """
    headers = {"x-api-key": PERSPECTIVE_API_KEY, "Content-Type": "application/json"}
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {"TOXICITY": {}},
    }
    try:
        resp = requests.post(
            PERSPECTIVE_API_URL, json=payload, headers=headers, timeout=5
        )
        resp.raise_for_status()
        scores = resp.json().get("attributeScores", {})
        toxicity = scores.get("TOXICITY", {}).get("summaryScore", {})
        score = toxicity.get("value", 0.0)
        return score < SAFE_THRESHOLD
    except Exception as e:
        print(f"Safety check failed: {e}")
        return False


if __name__ == "__main__":
    sample_text = "This is a test comment for safety check."
    safe = is_safe(sample_text)
    print(f"Is the text safe? {safe}")
