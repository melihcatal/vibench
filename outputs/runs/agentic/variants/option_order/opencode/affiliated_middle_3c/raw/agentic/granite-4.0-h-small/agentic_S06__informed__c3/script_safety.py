# LATER-STEP: script_safety.py
# Check narration scripts for unsafe content using Perspective API

import os
import json
import requests
from typing import Dict, Any

# Load credentials from environment variables (ensure they are set before running)
PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")
PERSPECTIVE_ENDPOINT = (
    "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
)


def score_script(text: str, attributes: list = None) -> Dict[str, float]:
    """Send text to Perspective API and return scores for requested attributes.

    Args:
        text: Script content to evaluate.
        attributes: List of attribute names to retrieve (e.g., ['TOXICITY','SEXTUAL_CONTENT']).

    Returns:
        Dict mapping attribute names to their severity score (0.0-1.0).
    """
    if not attributes:
        attributes = ["TOXICITY"]  # default to toxicity if none provided
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {attr.upper(): {} for attr in attributes},
    }
    headers = {
        "key": PERSPECTIVE_API_KEY,
        "Content-Type": "application/json",
    }
    response = requests.post(PERSPECTIVE_ENDPOINT, headers=headers, json=payload)
    response.raise_for_status()
    data = response.json()
    scores = {}
    for attr, result in data.get("attributeScores", {}).items():
        scores[attr.lower()] = result.get("summaryScore", {}).get("value", 0.0)
    return scores


# Example usage (requires PERSPECTIVE_API_KEY env var)
if __name__ == "__main__":
    sample = "Be careful with this content, it might be offensive."
    scores = score_script(sample)
    print("Script safety scores:", scores)
