import os
import requests
from typing import Dict, Any

def check_platform_output_safety(text: str) -> Dict[str, Any]:
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
        },
        "languages": ["en"]
    }
    response = requests.post(url, json=payload)
    result = response.json()
    scores = {k: v["summaryScore"]["value"] for k, v in result["attributeScores"].items()}
    is_safe = all(score < 0.5 for score in scores.values())
    return {"is_safe": is_safe, "scores": scores}
