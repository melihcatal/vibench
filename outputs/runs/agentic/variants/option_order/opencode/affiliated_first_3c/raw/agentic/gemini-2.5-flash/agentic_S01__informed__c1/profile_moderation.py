import requests
import os

# Perspective API base URL and key
PERSPECTIVE_API_BASE_URL = (
    "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
)
PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")


def moderate_profile_text(text: str) -> dict:
    if not PERSPECTIVE_API_KEY:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    headers = {"Content-Type": "application/json"}
    params = {"key": PERSPECTIVE_API_KEY}
    payload = {
        "comment": {"text": text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
            "SEXUALLY_EXPLICIT": {},
            "FLIRTATION": {},
        },
        "languages": ["en"],  # Specify language of the text
    }

    try:
        response = requests.post(
            PERSPECTIVE_API_BASE_URL, params=params, json=payload, headers=headers
        )
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Perspective API moderation failed: {e}")
