import os
import requests

PERSPECTIVE_API_KEY = os.environ.get("PERSPECTIVE_API_KEY")
PERSPECTIVE_API_BASE_URL = (
    "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
)


def check_text_safety_perspective(text: str) -> dict:
    if not PERSPECTIVE_API_KEY:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    params = {"key": PERSPECTIVE_API_KEY}
    data = {"comment": {"text": text}, "requestedAttributes": {"TOXICITY": {}}}
    headers = {"Content-Type": "application/json"}

    response = requests.post(
        PERSPECTIVE_API_BASE_URL, params=params, json=data, headers=headers
    )
    response.raise_for_status()
    return response.json()
