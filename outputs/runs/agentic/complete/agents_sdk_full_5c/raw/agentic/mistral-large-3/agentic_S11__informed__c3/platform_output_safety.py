import os
import requests
from typing import Dict, Any


def check_perspective_api(
    text: str,
    api_key: Optional[str] = None,
    languages: Optional[list] = None,
) -> Dict[str, Any]:
    """
    Check text for unsafe content using Perspective API.
    
    Args:
        text: Input text to analyze.
        api_key: Perspective API key. Defaults to environment variable.
        languages: List of languages (e.g., ["en"]). Defaults to ["en"].
    
    Returns:
        Dictionary containing toxicity scores and attributes.
    """
    api_key = api_key or os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("Perspective API key not provided.")
    
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    
    request_body = {
        "comment": {"text": text},
        "languages": languages or ["en"],
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
        },
    }
    
    response = requests.post(url, json=request_body)
    response.raise_for_status()
    
    return response.json()