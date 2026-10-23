import os
import requests
from typing import Dict, Any, List
from dataclasses import dataclass


@dataclass
class SafetyCheckResult:
    is_safe: bool
    categories: Dict[str, float]
    raw_response: Optional[Dict] = None


def check_platform_output_safety(text: str) -> SafetyCheckResult:
    """
    Check platform model output for unsafe content using Perspective API.
    """
    api_key = os.getenv("PERSPECTIVE_API_KEY")
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

    try:
        response = requests.post(url, params=params, json=payload)
        response.raise_for_status()
        data = response.json()

        categories = {}
        for attr_name, attr_data in data.get("attributeScores", {}).items():
            categories[attr_name] = attr_data.get("summaryScore", {}).get("value", 0.0)

        is_safe = all(score < 0.7 for score in categories.values())

        return SafetyCheckResult(
            is_safe=is_safe, categories=categories, raw_response=data
        )
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to check safety with Perspective API: {e}")
