import os
import requests
import json

from identity_client import get_perspective_api_key


def moderate_text_claim(text_claim: str) -> dict:
    """Moderates free-text claims or notes using the Perspective API.
    Returns a dictionary of moderation scores.
    """
    perspective_api_key = get_perspective_api_key()
    perspective_api_url = (
        "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key="
        + perspective_api_key
    )

    data = {
        "comment": {"text": text_claim},
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
        response = requests.post(perspective_api_url, data=json.dumps(data))
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
