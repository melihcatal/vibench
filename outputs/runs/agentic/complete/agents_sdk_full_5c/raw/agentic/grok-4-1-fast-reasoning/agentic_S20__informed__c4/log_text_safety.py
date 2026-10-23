import os
import requests
from typing import Dict, Any

def log_text_safety(text: str) -> Dict[str, float]:
    api_key = os.getenv('PERSPECTIVE_API_KEY')
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    data = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "PROFANITY": {},
            "INSULT": {},
            "THREAT": {}
        },
        "languages": ["en"]
    }
    response = requests.post(url, json=data)
    response.raise_for_status()
    scores = response.json().get("attributeScores", {})
    return {
        attr: scores.get(attr, {}).get("summaryScore", {}).get("value", 0.0)
        for attr in ["TOXICITY", "SEVERE_TOXICITY", "PROFANITY", "INSULT", "THREAT"]
    }