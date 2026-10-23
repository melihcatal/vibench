from typing import Dict, List
import os
import requests


def check_script_safety(text: str) -> Dict[str, float]:
    """
    Check narration scripts for unsafe content using Perspective API.
    """
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set")
    
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    data = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {}
        },
        "languages": ["en"]
    }
    
    response = requests.post(url, json=data)
    response.raise_for_status()
    result = response.json()
    
    attributes = result.get("attributeScores", {})
    scores = {attr: details["summaryScore"]["value"] for attr, details in attributes.items()}
    
    return scores