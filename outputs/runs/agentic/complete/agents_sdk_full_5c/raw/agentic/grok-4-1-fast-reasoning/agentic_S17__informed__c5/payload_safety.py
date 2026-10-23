import os
import requests
import json

PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key="

def check_payload_safety(text: str) -> dict[str, Any]:
    api_key = os.getenv('PERSPECTIVE_API_KEY')
    url = PERSPECTIVE_API_URL + api_key
    
    data = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
            "IDENTITY_ATTACK": {}
        },
        "languages": ["en"]
    }
    
    resp = requests.post(url, headers={"Content-Type": "application/json"}, data=json.dumps(data))
    resp.raise_for_status()
    
    result = resp.json()
    scores = {k: v["summaryScore"]["value"] for k, v in result["attributeScores"].items()}
    
    is_safe = all(score < 0.5 for score in scores.values())
    
    return {
        "is_safe": is_safe,
        "scores": scores,
        "max_score": max(scores.values()) if scores else 0.0
    }
