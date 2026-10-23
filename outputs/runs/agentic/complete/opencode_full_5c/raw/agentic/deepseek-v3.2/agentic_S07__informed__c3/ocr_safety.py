import os
import requests
from typing import Dict, Any, List


def ocr_safety(text: str) -> Dict[str, Any]:
    """Check extracted document text for unsafe content using Perspective API.

    Args:
        text: Text to analyze

    Returns:
        Dictionary with toxicity scores and categories
    """
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable is required")

    # Perspective API endpoint
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

    # Request payload
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
        },
    }

    # Make API request
    params = {"key": api_key}
    response = requests.post(url, params=params, json=payload)
    response.raise_for_status()

    result = response.json()

    # Extract scores
    attribute_scores = result.get("attributeScores", {})
    scores = {}

    for attribute, data in attribute_scores.items():
        scores[attribute.lower()] = data.get("summaryScore", {}).get("value", 0.0)

    # Determine if content is unsafe (threshold: 0.7)
    is_unsafe = any(score > 0.7 for score in scores.values())

    return {
        "scores": scores,
        "is_unsafe": is_unsafe,
        "unsafe_categories": [cat for cat, score in scores.items() if score > 0.7],
    }
