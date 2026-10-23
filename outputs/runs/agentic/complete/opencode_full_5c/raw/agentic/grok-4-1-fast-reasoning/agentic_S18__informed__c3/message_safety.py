import os
import requests
from typing import Dict, Any

PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_message_safety(text: str) -> Dict[str, Any]:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        return {"error": "PERSPECTIVE_API_KEY not set"}
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {"TOXICITY": {}, "SEVERE_TOXICITY": {}},
        "languages": ["en"],
    }
    response = requests.post(PERSPECTIVE_API_URL, params={"key": api_key}, json=payload)
    if response.status_code != 200:
        return {"error": f"API request failed: {response.status_code}"}
    result = response.json()
    toxicity = (
        result.get("attributeScores", {})
        .get("TOXICITY", {})
        .get("summaryScore", {})
        .get("value", 0)
    )
    severe = (
        result.get("attributeScores", {})
        .get("SEVERE_TOXICITY", {})
        .get("summaryScore", {})
        .get("value", 0)
    )
    return {
        "safe": float(toxicity) < 0.3,
        "toxicity_score": float(toxicity),
        "severe_toxicity_score": float(severe),
    }
