import os
import requests
import json
from typing import Dict

PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

def moderate_transcript(text: str) -> Dict[str, float]:
    api_key = os.getenv('PERSPECTIVE_API_KEY')
    if not api_key:
        raise ValueError('PERSPECTIVE_API_KEY environment variable is required.')
    
    data = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {}
        },
        "languages": ["en"]
    }
    
    response = requests.post(
        f"{PERSPECTIVE_API_URL}?key={api_key}",
        headers={"Content-Type": "application/json"},
        data=json.dumps(data)
    )
    response.raise_for_status()
    result = response.json()
    
    scores = {}
    for attr, summary in result["attributeScores"].items():
        scores[attr.lower()] = summary["summaryScore"]["value"]
    
    return scores