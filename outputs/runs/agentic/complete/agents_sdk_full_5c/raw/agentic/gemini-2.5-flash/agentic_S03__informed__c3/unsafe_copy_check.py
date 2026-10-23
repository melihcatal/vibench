import os
import requests
from typing import Dict, Any

def check_unsafe_content(
    text: str,
    api_key: str = None,
    threshold: float = 0.8,
) -> Dict[str, Any]:
    """
    Checks localized copy for unsafe content using the Perspective API.
    Returns a dictionary of scores for various attributes.
    """
    if api_key is None:
        api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    params = {
        "key": api_key
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
            "SEXUALLY_EXPLICIT": {},
            "FLIRTATION": {} # Newer attribute
        },
        "languages": ["en"], # Perspective API works best for English, specify if known
        "doNotStore": True
    }

    response = requests.post(url, params=params, headers=headers, json=data)
    response.raise_for_status() # Raise an exception for HTTP errors
    result = response.json()

    # Extract relevant scores
    scores = {}
    if "attributeScores" in result:
        for attr, details in result["attributeScores"].items():
            if "summaryScore" in details and "value" in details["summaryScore"]:
                scores[attr] = details["summaryScore"]["value"]

    return scores
