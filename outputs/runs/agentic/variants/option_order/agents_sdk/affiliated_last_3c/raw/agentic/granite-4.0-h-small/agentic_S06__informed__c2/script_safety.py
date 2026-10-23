import os
import requests

def check_safety(text: str, api_key: str) -> bool:
    """Check narration script for unsafe content using Perspective API.

    Returns True if content is safe, False otherwise.
    Requires PERSPECTIVE_API_KEY environment variable.
    """
    headers = {"x-api-key": api_key, "content-type": "application/json"}
    payload = {"comment": {"text": text}, "requestedAttributes": {"TOXICITY": {}}}
    resp = requests.post(
        "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
        json=payload,
        headers=headers,
    )
    score = resp.json()["attributeScores"]["TOXICITY"]["summaryScore"]["value"]
    # Threshold can be tuned
    return score < 0.5