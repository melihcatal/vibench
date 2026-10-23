import os
import requests
from typing import Dict, Any


def check_prompt_safety(prompt: str) -> Dict[str, Any]:
    """Check prompt for unsafe content using Perspective API."""
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable is required")

    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

    params = {"key": api_key}

    data = {
        "comment": {"text": prompt},
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

    response = requests.post(url, params=params, json=data)
    response.raise_for_status()

    result = response.json()

    scores = {}
    for attribute_name, attribute_data in result.get("attributeScores", {}).items():
        scores[attribute_name] = attribute_data.get("summaryScore", {}).get("value", 0)

    is_safe = all(score < 0.7 for score in scores.values())

    return {"is_safe": is_safe, "scores": scores, "raw_response": result}
