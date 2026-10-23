import os
import requests
from typing import Dict

def check_script_safety(script: str, threshold: float = 0.5) -> Dict[str, float]:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set")
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    payload = {
        "comment": {"text": script},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {}
        },
        "languages": ["en"]
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    result = response.json()
    scores = result["attributeScores"]
    toxicity = scores["TOXICITY"]["summaryScore"]["value"]
    return {
        "toxicity": toxicity,
        "severe_toxicity": scores["SEVERE_TOXICITY"]["summaryScore"]["value"],
        "is_unsafe": toxicity > threshold
    }