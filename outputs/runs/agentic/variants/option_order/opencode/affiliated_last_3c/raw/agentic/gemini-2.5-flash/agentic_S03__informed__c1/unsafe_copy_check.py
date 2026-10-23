import requests
import os
from translation_models import UnsafeCopyCheckRequest

# Perspective API endpoint and key
PERSPECTIVE_API_BASE_URL = (
    "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
)
PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY")


def check_unsafe_content(request: UnsafeCopyCheckRequest) -> dict:
    if not PERSPECTIVE_API_KEY:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    headers = {"Content-Type": "application/json"}
    params = {"key": PERSPECTIVE_API_KEY}

    payload = {
        "comment": {"text": request.text},
        "requestedAttributes": {
            "TOXICITY": {},
            "SEVERE_TOXICITY": {},
            "IDENTITY_ATTACK": {},
            "INSULT": {},
            "PROFANITY": {},
            "THREAT": {},
        },
        "languages": request.languages if request.languages else None,
    }

    response = requests.post(
        PERSPECTIVE_API_BASE_URL, headers=headers, params=params, json=payload
    )
    response.raise_for_status()

    return response.json()
