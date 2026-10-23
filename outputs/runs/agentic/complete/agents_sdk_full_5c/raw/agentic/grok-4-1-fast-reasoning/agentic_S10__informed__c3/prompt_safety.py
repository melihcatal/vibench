import os
import requests
from typing import Dict

def check_safety(text: str) -> Dict[str, float]:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY not set")
    
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
            "SEXUALLY_EXPLICIT": {},
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
    return scores

def is_unsafe(text: str, threshold: float = 0.7) -> bool:
    scores = check_safety(text)
    return any(score >= threshold for score in scores.values())