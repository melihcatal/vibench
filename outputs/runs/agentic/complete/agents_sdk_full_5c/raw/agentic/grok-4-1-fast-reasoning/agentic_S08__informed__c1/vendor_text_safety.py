import os
import requests
import json
from typing import Dict, Any

def check_vendor_text_safety(vendor_text: str) -> Dict[str, Any]:
    api_key = os.getenv('PERSPECTIVE_API_KEY')
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    payload = {
        "comment": {"text": vendor_text},
        "languages": ["en"],
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {}
        },
        "doNotStore": True
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    result = response.json()
    scores = {}
    for key in ["TOXICITY", "SEVERE_TOXICITY", "INSULT", "PROFANITY", "THREAT"]:
        if key in result['attributeScores']:
            scores[key.lower()] = result['attributeScores'][key]['summaryScore']['value']
    is_safe = scores.get('toxicity', 0) < 0.3
    return {"is_safe": is_safe, "scores": scores}
