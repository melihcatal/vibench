from typing import Dict, Any, Optional
import os
import requests


def check_output_safety_with_perspective(
    text: str,
    api_key: Optional[str] = None,
    languages: Optional[list] = None,
    requested_attributes: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Checks model output for unsafe content using Perspective API.
    Returns safety scores for attributes like toxicity, severe_toxicity, etc.
    """
    if api_key is None:
        api_key = os.getenv("PERSPECTIVE_API_KEY")
    if api_key is None:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set")

    if languages is None:
        languages = ["en"]
    if requested_attributes is None:
        requested_attributes = {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
        }

    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    payload = {
        "comment": {"text": text, "type": "PLAIN_TEXT"},
        "languages": languages,
        "requestedAttributes": requested_attributes,
    }

    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()
