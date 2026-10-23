import os
import requests
from typing import Dict, Any


def unsafe_copy_check(text: str, lang: str) -> Dict[str, Any]:
    """
    Checks localized copy for unsafe content using the Perspective API.
    """
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"

    payload = {
        "comment": {"text": text},
        "languages": [lang],
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
        },
    }

    response = requests.post(url, json=payload, timeout=10)
    response.raise_for_status()

    data = response.json()
    summary = {
        attr: data["attributeScores"][attr]["summaryScore"]["value"]
        for attr in data["attributeScores"]
    }
    return summary
