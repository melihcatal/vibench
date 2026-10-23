import os
from typing import Any
import requests


def check_script_for_safety(script: str, api_key: str) -> bool:
    """Check narration script for unsafe content using Perspective API.

    Returns True if content is acceptable, False otherwise.
    """
    endpoint = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    headers = {
        "content-type": "application/json",
        "x-goog-api-key": api_key,
    }
    payload = {
        "comment": {"text": script},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
        },
    }
    response = requests.post(endpoint, json=payload, headers=headers)
    if response.status_code != 200:
        raise RuntimeError(f"Perspective API error: {response.text}")
    result = response.json()
    # If any severe attribute score >= 0.8, reject
    toxicity = (
        result.get("attributeScores", {}).get("TOXICITY", {}).get("summaryScore", {})
    )  # type: ignore
    if toxicity and toxicity.get("value", 0.0) >= 0.8:
        return False
    # Severe toxicity check
    severe = (
        result.get("attributeScores", {})
        .get("SEVERE_TOXICITY", {})
        .get("summaryScore", {})
    )  # type: ignore
    if severe and severe.get("value", 0.0) >= 0.8:
        return False
    return True


# Example usage (never commit real API key to source control):
# check_script_for_safety(script_text, api_key=os.getenv('PERSPECTIVE_API_KEY'))
