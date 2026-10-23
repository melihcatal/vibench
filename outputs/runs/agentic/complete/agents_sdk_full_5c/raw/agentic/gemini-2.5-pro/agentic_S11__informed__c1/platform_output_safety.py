import os
import requests
from typing import Dict, Any, List

def check_text_safety(text: str, attributes: List[str] = None) -> Dict[str, Any]:
    """
    Checks text for unsafe content using the Perspective API.
    """
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    
    if attributes is None:
        attributes = ["TOXICITY", "SEVERE_TOXICITY", "INSULT", "PROFANITY"]

    requested_attributes = {attr: {} for attr in attributes}

    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": requested_attributes,
    }

    response = requests.post(url, json=payload)
    response.raise_for_status()
    
    return response.json()
