import os
import requests
from typing import Dict, Any, List


def check_localized_copy_safety(text: str, language_code: str = "en") -> Dict[str, Any]:
    """
    Check localized copy for unsafe content using Perspective API.

    Args:
        text: Text to check for unsafe content
        language_code: Language code of the text

    Returns:
        Dictionary with safety scores and flags
    """
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable is required")

    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"

    payload = {
        "comment": {"text": text},
        "languages": [language_code],
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
        },
    }

    response = requests.post(url, json=payload)
    response.raise_for_status()
    result = response.json()

    attribute_scores = result.get("attributeScores", {})

    safety_scores = {}
    for attribute_name, attribute_data in attribute_scores.items():
        summary_score = attribute_data.get("summaryScore", {})
        safety_scores[attribute_name.lower()] = {
            "score": summary_score.get("value", 0),
            "type": summary_score.get("type", "UNKNOWN"),
        }

    max_toxicity = (
        max([score["score"] for score in safety_scores.values()])
        if safety_scores
        else 0
    )

    return {
        "text": text,
        "language": language_code,
        "safety_scores": safety_scores,
        "is_unsafe": max_toxicity > 0.7,
        "unsafe_threshold": 0.7,
        "max_toxicity_score": max_toxicity,
        "provider": "perspective-api",
        "api_endpoint": "commentanalyzer.googleapis.com",
    }
