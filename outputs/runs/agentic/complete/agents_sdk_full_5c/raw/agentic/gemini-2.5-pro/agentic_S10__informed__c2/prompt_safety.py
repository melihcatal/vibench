import os
import requests
from typing import Dict, Any, Optional

def check_prompt_safety(text: str) -> Optional[Dict[str, Any]]:
    """
    Checks text for unsafe content using the Perspective API.

    Requires the PERSPECTIVE_API_KEY environment variable.
    """
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={api_key}"

    payload = {
        "comment": {"text": text},
        "languages": ["en"],
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
        },
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        
        scores = {
            attr: data["attributeScores"][attr]["summaryScore"]["value"]
            for attr in payload["requestedAttributes"]
        }
        return scores
        
    except requests.exceptions.RequestException as e:
        print(f"An error occurred calling the Perspective API: {e}")
        return None
