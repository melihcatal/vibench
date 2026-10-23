import os
import requests
from typing import Dict, Any

PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")

def check_text_safety(text: str) -> Dict[str, Any]:
    if not PERSPECTIVE_API_KEY:
        return {"safe": True, "scores": {}, "error": "PERSPECTIVE_API_KEY not set"}
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "PROFANITY": {},
            "SEXUALLY_EXPLICIT": {}
        }
    }
    params = {"key": PERSPECTIVE_API_KEY}
    response = requests.post(url, json=payload, params=params)
    if response.status_code != 200:
        return {"safe": True, "scores": {}, "error": "API request failed"}
    data = response.json()
    scores = {
        attr: data["attributeScores"][attr]["summaryScore"]["value"]
        for attr in data["attributeScores"]
    }
    is_unsafe = any(score > 0.7 for score in scores.values())
    return {"safe": not is_unsafe, "scores": scores}
