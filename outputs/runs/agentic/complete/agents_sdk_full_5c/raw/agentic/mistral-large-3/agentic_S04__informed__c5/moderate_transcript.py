import os
from typing import List, Dict
import requests

def moderate_transcript(segments: List[Dict[str, str]]) -> List[Dict[str, Any]]:
    """
    Moderates transcript text using Perspective API.
    Returns moderation results for each segment.
    """
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")
    
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    headers = {"Content-Type": "application/json"}
    
    results = []
    
    for segment in segments:
        data = {
            "comment": {"text": segment["text"]},
            "requestedAttributes": {
                "TOXICITY": {},
                "SEVERE_TOXICITY": {},
                "IDENTITY_ATTACK": {}
            }
        }
        
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        
        results.append({
            **segment,
            "moderation": response.json()["attributeScores"]
        })
    
    return results