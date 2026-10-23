import os
from typing import List
import requests


def check_text_safety(texts: List[str]) -> List[bool]:
    """Check corpus text for safety using Perspective API."""
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set")
    
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    results = []
    
    for text in texts:
        payload = {
            "comment": {"text": text},
            "requestedAttributes": {"TOXICITY": {}},
            "languages": ["en"]
        }
        response = requests.post(url, json=payload)
        if response.status_code != 200:
            raise RuntimeError(f"Perspective API error: {response.text}")
        
        toxicity_score = response.json().get("attributeScores", {}).get("TOXICITY", {}).get("summaryScore", {}).get("value", 0.0)
        results.append(toxicity_score < 0.7)
    
    return results