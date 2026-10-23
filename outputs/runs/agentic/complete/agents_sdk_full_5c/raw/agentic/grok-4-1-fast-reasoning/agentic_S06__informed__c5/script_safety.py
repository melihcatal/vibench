import os
import requests
from typing import Dict, Any

PERSPECTIVE_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

def check_script_safety(script: str, threshold: float = 0.5) -> Dict[str, Any]:
    """
    Checks narration scripts for unsafe content using Perspective API.
    """
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable is required.")
    
    data = {
        "comment": {"text": script},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {}
        },
        "languages": ["en"]
    }
    
    response = requests.post(f"{PERSPECTIVE_URL}?key={api_key}", json=data)
    response.raise_for_status()
    
    result = response.json()
    scores = {
        attr: result["attributeScores"][attr]["summaryScore"]["value"]
        for attr in data["requestedAttributes"]
    }
    is_safe = all(scores[attr] < threshold for attr in scores)
    
    return {
        "is_safe": is_safe,
        "scores": scores,
        "analysis": result
    }