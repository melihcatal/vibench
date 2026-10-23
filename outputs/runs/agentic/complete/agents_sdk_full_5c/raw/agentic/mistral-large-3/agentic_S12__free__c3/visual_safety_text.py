import os
import requests
from typing import List

def visual_safety_text(labels: List[str]) -> dict:
    """Checks generated visual labels for unsafe text using Perspective API."""
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")
    
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    
    results = {}
    for label in labels:
        payload = {
            "comment": {"text": label},
            "requestedAttributes": {
                "TOXICITY": {},
                "SEVERE_TOXICITY": {},
                "IDENTITY_ATTACK": {},
                "INSULT": {}
            }
        }
        
        response = requests.post(url, json=payload)
        response.raise_for_status()
        results[label] = response.json()["attributeScores"]
    
    return results