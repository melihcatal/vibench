import os
import json
import requests
from typing import Dict, Any


def check_script_for_unsafe_content(text: str) -> Dict[str, float]:
    """
    Checks narration scripts for unsafe content using the Google Perspective API.

    Requires the PERSPECTIVE_API_KEY environment variable.

    Args:
        text: The script text to analyze.

    Returns:
        A dictionary of toxicity attributes and their scores.
    """
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not found.")

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
        response = requests.post(url, data=json.dumps(payload))
        response.raise_for_status()
        response_data = response.json()
        
        scores = {
            attr: scores["summaryScore"]["value"]
            for attr, scores in response_data["attributeScores"].items()
        }
        return scores

    except requests.exceptions.RequestException as e:
        print(f"Failed to call Perspective API: {e}")
        raise
    except (KeyError, IndexError) as e:
        print(f"Could not parse Perspective API response: {e}")
        raise
