import os
import requests
from typing import Dict, Any

def log_text_safety(log_text: str) -> Dict[str, Any]:
    """
    Checks log message text for unsafe content using Google Perspective API.
    """
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    payload = {
        "comment": {"text": log_text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "PROFANITY": {},
            "THREAT": {}
        },
        "languages": ["en"]
    }
    response = requests.post(url, json=payload)
    if response.status_code != 200:
        return {"error": "API request failed", "status_code": response.status_code}
    result = response.json()
    scores = {
        attr: result["attributeScores"][attr]["summaryScore"]["value"]
        for attr in payload["requestedAttributes"]
    }
    flagged = any(score > 0.7 for score in scores.values())
    return {
        "flagged": flagged,
        "scores": scores
    }
