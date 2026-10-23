import requests
import os
from typing import Dict, List, Any


def check_localized_copy_safety(text: str, language_code: str = "en") -> Dict[str, Any]:
    """
    Check localized copy for unsafe content using Perspective API.

    Args:
        text: Text to check for unsafe content
        language_code: Language code of the text

    Returns:
        Dictionary with safety analysis results
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
        safety_scores[attribute_name] = {
            "value": summary_score.get("value", 0),
            "type": summary_score.get("type", "UNKNOWN"),
        }

    max_toxicity = max(
        safety_scores.get("TOXICITY", {}).get("value", 0),
        safety_scores.get("SEVERE_TOXICITY", {}).get("value", 0),
    )

    is_unsafe = max_toxicity > 0.7

    return {
        "text": text,
        "language_code": language_code,
        "safety_scores": safety_scores,
        "is_unsafe": is_unsafe,
        "max_toxicity_score": max_toxicity,
        "provider": "Perspective API",
    }
