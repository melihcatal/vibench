import os
import requests
from typing import Dict, Any, List


def check_script_safety(text: str) -> Dict[str, Any]:
    """Check narration scripts for unsafe content using Perspective API."""
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set")

    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"

    payload = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
        },
        "languages": ["en"],
    }

    response = requests.post(url, json=payload)
    response.raise_for_status()

    return response.json()


def batch_check_scripts(scripts: List[str]) -> List[Dict[str, Any]]:
    """Check a batch of narration scripts for unsafe content using Perspective API."""
    return [check_script_safety(script) for script in scripts]
