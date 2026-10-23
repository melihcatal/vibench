import requests
import os
import json
from typing import Dict, Any

def log_text_safety(text: str) -> Dict[str, float]:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {}
        }
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    result = response.json()
    scores = {
        attr: result["attributeScores"][attr]["summaryScore"]["value"]
        for attr in result["attributeScores"]
    }
    return scores