import os
import requests
from typing import Dict, Any, List


def check_labels_for_unsafe_text(labels: List[str]) -> Dict[str, Any]:
    """
    Check generated visual labels for unsafe text using Perspective API.

    Args:
        labels: List of label names to check

    Returns:
        Dictionary containing safety analysis results
    """
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set")

    text_to_check = " ".join(labels)

    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    params = {"key": api_key}

    payload = {
        "comment": {"text": text_to_check},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
        },
        "languages": ["en"],
    }

    response = requests.post(url, params=params, json=payload)
    response.raise_for_status()
    result = response.json()

    attribute_scores = result.get("attributeScores", {})

    scores = {}
    for attribute, data in attribute_scores.items():
        scores[attribute] = data["summaryScore"]["value"]

    max_score = max(scores.values()) if scores else 0.0
    is_safe = max_score < 0.7

    return {
        "is_safe": is_safe,
        "scores": scores,
        "max_score": max_score,
        "text_checked": text_to_check,
    }
