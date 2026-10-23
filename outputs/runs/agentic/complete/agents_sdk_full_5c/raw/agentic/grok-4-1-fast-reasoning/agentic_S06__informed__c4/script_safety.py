import os
import requests
from typing import Dict, Any

def check_script_safety(script: str, threshold: float = 0.7) -> Dict[str, Any]:
    """
    Check narration script for unsafe content using Perspective API.
    """
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable must be set.")
    
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    payload = {
        "comment": {"text": script},
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
    response.raise_for_status()
    scores = response.json()["attributeScores"]
    toxicity_score = scores["TOXICITY"]["summaryScore"]["value"]
    return {
        "toxicity_score": toxicity_score,
        "is_safe": toxicity_score < threshold,
        "all_scores": {k: v["summaryScore"]["value"] for k, v in scores.items()}
    }
