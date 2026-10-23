import os
import requests
from typing import Dict, Any

def check_platform_output_safety(text: str) -> Dict[str, Any]:
    """
    Check platform model output for unsafe content using Perspective API.
    """
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable is required")
    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "INSULT": {},
            "PROFANE": {},
            "IDENTITY_ATTACK": {},
            "THREAT": {}
        },
        "doNotStore": True
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    result = response.json()
    # Simplify scores
    scores = {k: v["summaryScore"]["value"] for k, v in result["attributeScores"].items()}
    return {
        "safe": all(score < 0.5 for score in scores.values()),
        "scores": scores,
        "raw": result
    }
