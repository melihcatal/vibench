import os
import requests


def check_content_safety(text):
    """Check narration scripts for unsafe content using Perspective API."""
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable is required")

    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

    params = {"key": api_key}

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

    response = requests.post(url, params=params, json=payload)
    response.raise_for_status()

    result = response.json()

    safety_scores = {}
    for attribute_name, attribute_data in result.get("attributeScores", {}).items():
        safety_scores[attribute_name] = attribute_data.get("summaryScore", {}).get(
            "value", 0
        )

    is_safe = all(score < 0.7 for score in safety_scores.values())

    return {
        "is_safe": is_safe,
        "scores": safety_scores,
        "flagged_attributes": [
            attr for attr, score in safety_scores.items() if score >= 0.7
        ],
    }
