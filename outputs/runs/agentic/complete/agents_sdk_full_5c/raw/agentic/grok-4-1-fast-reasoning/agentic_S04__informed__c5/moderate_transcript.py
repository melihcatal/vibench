import os
import requests
import json
from typing import Dict

def moderate_transcript(text: str) -> Dict[str, any]:
    """
    Moderate transcript text using Perspective API before publishing.
    Returns safety scores.
    """
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable is not set")
    
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
        },
        "languages": ["en"]
    }
    
    response = requests.post(url, json=payload)
    response.raise_for_status()
    
    result = response.json()
    scores = {
        attr: result["attributeScores"][attr]["summaryScore"]["value"]
        for attr in payload["requestedAttributes"]
    }
    
    return {
        "safe": all(score < 0.5 for score in scores.values()),
        "scores": scores
    }
