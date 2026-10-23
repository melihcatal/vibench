import os
import requests
from typing import Dict, Any

PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_annotation_safety(text: str) -> Dict[str, Any]:
    """
    Checks the safety of a text annotation using the Perspective API.
    """
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    params = {"key": api_key}

    request_body = {
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
        response = requests.post(
            PERSPECTIVE_API_URL, params=params, json=request_body, timeout=10
        )
        response.raise_for_status()

        response_data = response.json()
        scores = {
            attr: response_data["attributeScores"][attr]["summaryScore"]["value"]
            for attr in response_data["attributeScores"]
        }
        return scores

    except requests.exceptions.RequestException as e:
        return {"error": f"Perspective API request failed: {e}"}
