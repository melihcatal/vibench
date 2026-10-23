import os
import requests
from typing import Dict, Any

def message_safety(text: str) -> Dict[str, float]:
    """
    Checks message payload text for unsafe content using Perspective API.
    """
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable is required.")
    
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}, "SEVERE_TOXICITY": {}}
    }
    
    response = requests.post(url, json=payload)
    response.raise_for_status()
    
    result = response.json()
    scores = {
        "toxicity": result["attributeScores"]["TOXICITY"]["summaryScore"]["value"],
        "severe_toxicity": result["attributeScores"]["SEVERE_TOXICITY"]["summaryScore"]["value"]
    }
    return scores