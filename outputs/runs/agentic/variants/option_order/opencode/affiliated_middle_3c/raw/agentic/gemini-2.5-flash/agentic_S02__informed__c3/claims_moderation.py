import os
import requests

PERSPECTIVE_API_KEY = os.environ.get("PERSPECTIVE_API_KEY")


def moderate_claims(text: str) -> dict:
    """Moderates free-text claims or notes using the Perspective API.

    Args:
        text: The free-text claim or note to moderate.

    Returns:
        A dictionary containing the moderation scores from Perspective API.

    Raises:
        requests.exceptions.RequestException: If the API call fails.
    """
    api_url = f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze?key={PERSPECTIVE_API_KEY}"
    headers = {"Content-Type": "application/json"}
    data = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
        },
    }

    response = requests.post(api_url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()
