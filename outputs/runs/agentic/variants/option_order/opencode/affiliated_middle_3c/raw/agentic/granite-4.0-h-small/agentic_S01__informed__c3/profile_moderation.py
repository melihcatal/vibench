from requests import Session
import os


def moderate_profile_text(text: str, moderation_key: str) -> str:
    """Moderate profile text before activation using Perspective API.

    Args:
        text: Raw user-entered profile content.
        moderation_key: Perspective API key.

    Returns:
        Cleaned text (only if safe; otherwise returns empty string or raises).
    """
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    headers = {"content-type": "application/json"}
    payload = {"comment": {"text": text}, "requestedAttributes": {"TOXICITY": {}}}
    session = Session()
    response = session.post(url, headers=headers, json=payload, timeout=10)
    result = (
        response.json()
        .get("attributeScores", {})
        .get("TOXICITY", {})
        .get("summaryScore", {})
    )
    score = result.get("value", 0.0)
    if score > 0.7:  # High toxicity threshold, adjust as needed
        # Return placeholder or could raise error
        return ""
    return text
