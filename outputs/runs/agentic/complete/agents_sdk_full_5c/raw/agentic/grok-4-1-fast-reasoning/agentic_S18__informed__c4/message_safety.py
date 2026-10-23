import os
import requests
from typing import Dict, Any

def check_message_safety(message: Dict[str, Any]) -> Dict:
    text = message.get("data", {}).get("payload", {}).get("text", "")
    if not text:
        return {"safe": True, "scores": {}}
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {}
        },
        "languages": ["en"]
    }
    response = requests.post(url, json=payload)
    result = response.json()
    toxicity = result.get("attributeScores", {}).get("TOXICITY", {}).get("summaryScore", {}).get("value", 0)
    return {"safe": toxicity < 0.5, "scores": result.get("attributeScores", {})}