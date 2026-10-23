from typing import Dict, Any
import requests
import os

def check_output_safety(text: str) -> Dict[str, Any]:
    """
    Checks Cohere model output for unsafe content using Perspective API.
    Returns safety scores and flags for toxicity, profanity, etc.
    """
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("Perspective API key not provided.")

    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "PROFANITY": {},
            "IDENTITY_ATTACK": {},
            "THREAT": {},
        },
        "languages": ["en"],
    }

    response = requests.post(url, json=payload)
    response.raise_for_status()
    result = response.json()

    return {
        "safety_scores": result.get("attributeScores", {}),
        "provider": "perspective",
    }